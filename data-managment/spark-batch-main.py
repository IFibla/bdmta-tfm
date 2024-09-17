from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import col, lag, avg, stddev, min, max, expr, count
import pyspark.sql.functions as F
from delta import configure_spark_with_delta_pip
import pandas as pd

SESSION_TYPE = "race-redbull-ring-e3"
pd.options.mode.chained_assignment = None

# Initialize Spark session with Delta Lake configuration
spark = (
    SparkSession.builder.appName("DataDash")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
    .config("spark.sql.adaptive.enabled", True)
)
spark = configure_spark_with_delta_pip(spark).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")


# Helper function to read and process Delta tables
def read_delta_table(path, session_type_filter, start_col, end_col, driver_col):
    """Reads Delta table, renames columns, and calculates end column using lag function."""
    return (
        spark.read.format("delta")
        .load(path)
        .filter(col("session_type") == session_type_filter)
        .drop("session_type")
        .withColumnRenamed("session_time", start_col)
        .withColumnRenamed("driver", driver_col)
        .withColumn(
            end_col,
            lag(start_col, -1).over(Window.partitionBy(driver_col).orderBy(start_col)),
        )
        .na.drop(subset=[end_col])
    )


# Read laps and segments data
laps = read_delta_table(
    "delta/laps", SESSION_TYPE, "start_lap", "end_lap", "driver_lap"
)
segments = read_delta_table(
    "delta/segments",
    SESSION_TYPE,
    "start_segment",
    "end_segment",
    "driver_segment",
)

# Join laps with segments
joined_segments = laps.join(
    segments,
    (laps.driver_lap == segments.driver_segment)
    & (laps.start_lap < segments.start_segment)
    & (segments.start_segment < laps.end_lap),
    "inner",
)


# Helper function to read telemetry, status, or damage data
def read_data(path, session_type_filter, driver_col):
    """Reads data from Delta table and renames the driver column."""
    return (
        spark.read.format("delta")
        .load(path)
        .filter(col("session_type") == session_type_filter)
        .drop("session_type")
        .withColumnRenamed("driver", driver_col)
    )


# Read telemetry, status, and damage data
telemetry = read_data("delta/telemetry", SESSION_TYPE, "driver_telemetry")
status = read_data("delta/status", SESSION_TYPE, "driver_telemetry")
damage = read_data("delta/damage", SESSION_TYPE, "driver_telemetry")
motion = read_data("delta/motion", SESSION_TYPE, "driver_telemetry")

# Define excluded columns for aggregation
excluded_columns = [
    "driver",
    "start_lap",
    "end_lap",
    "start_segment",
    "end_segment",
    "driver_telemetry",
    "session_time",
]


# Helper function to process data with laps or segments
def process_data(
    data, ref_data, driver_col, ref_start_col, ref_end_col, ref_driver_col
):
    """Processes data by joining with reference data (laps or segments) and performing aggregations."""
    pipeline = data.join(
        ref_data,
        (col(driver_col) == col(ref_driver_col))
        & (col("session_time") > col(ref_start_col))
        & (col("session_time") < col(ref_end_col)),
        "inner",
    ).withColumnRenamed(ref_driver_col, "driver")

    if "segment" in pipeline.columns:
        pipeline = pipeline.groupby(
            "driver", "segment", ref_start_col, ref_end_col, "start_lap", "end_lap"
        )
    else:
        pipeline = pipeline.groupby("driver", ref_start_col, ref_end_col)

    return pipeline.agg(
        *[
            avg(col(c)).alias(f"mean_{c}")
            for c in data.columns
            if c not in excluded_columns
        ],
        *[
            stddev(col(c)).alias(f"stddev_{c}")
            for c in data.columns
            if c not in excluded_columns
        ],
        *[
            min(col(c)).alias(f"min_{c}")
            for c in data.columns
            if c not in excluded_columns
        ],
        *[
            max(col(c)).alias(f"max_{c}")
            for c in data.columns
            if c not in excluded_columns
        ],
        *[
            expr(f"percentile_approx({c}, 0.25)").alias(f"25th_percentile_{c}")
            for c in data.columns
            if c not in excluded_columns
        ],
        *[
            expr(f"percentile_approx({c}, 0.5)").alias(f"50th_percentile_{c}")
            for c in data.columns
            if c not in excluded_columns
        ],
        *[
            expr(f"percentile_approx({c}, 0.75)").alias(f"75th_percentile_{c}")
            for c in data.columns
            if c not in excluded_columns
        ],
    )


# Process telemetry, status, and damage data with laps
telemetry_with_laps = process_data(
    telemetry, laps, "driver_telemetry", "start_lap", "end_lap", "driver_lap"
)
status_with_laps = process_data(
    status, laps, "driver_telemetry", "start_lap", "end_lap", "driver_lap"
)
damage_with_laps = process_data(
    damage, laps, "driver_telemetry", "start_lap", "end_lap", "driver_lap"
)
motion_with_laps = process_data(
    motion, laps, "driver_telemetry", "start_lap", "end_lap", "driver_lap"
)

consolidated_df_laps = (
    telemetry_with_laps.join(
        status_with_laps, ["driver", "start_lap", "end_lap"], "inner"
    )
    .join(damage_with_laps, ["driver", "start_lap", "end_lap"], "inner")
    .join(motion_with_laps, ["driver", "start_lap", "end_lap"], "inner")
)

consolidated_df_laps.write.mode("overwrite").save("delta/lap_results")

telemetry_with_segments = process_data(
    telemetry,
    joined_segments,
    "driver_telemetry",
    "start_segment",
    "end_segment",
    "driver_segment",
)
status_with_segments = process_data(
    status,
    joined_segments,
    "driver_telemetry",
    "start_segment",
    "end_segment",
    "driver_segment",
)
damage_with_segments = process_data(
    damage,
    joined_segments,
    "driver_telemetry",
    "start_segment",
    "end_segment",
    "driver_segment",
)
motion_with_segments = process_data(
    motion,
    joined_segments,
    "driver_telemetry",
    "start_segment",
    "end_segment",
    "driver_segment",
)
# Join all processed data into one consolidated DataFrame
consolidated_df_segments = (
    telemetry_with_segments.join(
        status_with_segments,
        ["driver", "segment", "start_segment", "end_segment", "start_lap", "end_lap"],
        "inner",
    )
    .join(
        damage_with_segments,
        ["driver", "segment", "start_segment", "end_segment", "start_lap", "end_lap"],
        "inner",
    )
    .join(
        motion_with_segments,
        ["driver", "segment", "start_segment", "end_segment", "start_lap", "end_lap"],
        "inner",
    )
)

# Save the consolidated DataFrame
consolidated_df_segments.write.mode("overwrite").save("delta/segment_results")
