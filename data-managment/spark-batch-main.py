from pyspark.sql.session import SparkSession
from pyspark.sql.types import (
    ArrayType,
    MapType,
    FloatType,
    IntegerType,
    StringType,
)
from pyspark.sql.functions import (
    col,
    posexplode,
    udf,
    lit,
)
import pyspark.sql.functions as F
from pyspark.sql import Window
from packets import Packet
from track import Track
from delta import *
import pandas as pd
import sys

pd.options.mode.chained_assignment = None

## --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2,io.delta:delta-spark_2.12:3.2.0

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

laps = (
    spark.read.format("delta")
    .load("delta/laps")
    .filter(F.col("session_type") == "fp1-redbull-ring-e3")
    .drop("session_type")
    .withColumnRenamed("session_time", "start_lap")
    .withColumnRenamed("driver", "driver_lap")
    .withColumn(
        "end_lap",
        F.lag("start_lap", -1).over(
            Window.partitionBy("driver_lap").orderBy("start_lap")
        ),
    )
    .na.drop(subset=["end_lap"])
)


telemetry = (
    spark.read.format("delta")
    .load("delta/telemetry")
    .filter(F.col("session_type") == "fp1-redbull-ring-e3")
    .drop("session_type")
    .withColumnRenamed("driver", "driver_telemetry")
)

# Read and process status data
status = (
    spark.read.format("delta")
    .load("delta/status")
    .filter(F.col("session_type") == "fp1-redbull-ring-e3")
    .drop("session_type")
    .withColumnRenamed("driver", "driver_telemetry")
)

# Read and process damage data
damage = (
    spark.read.format("delta")
    .load("delta/damage")
    .filter(F.col("session_type") == "fp1-redbull-ring-e3")
    .drop("session_type")
    .withColumnRenamed("driver", "driver_telemetry")
)

excluded_columns = [
    "driver",
    "start_lap",
    "end_lap",
    "driver_telemetry",
    "session_time",
]

# Process telemetry data with laps
telemetry_with_laps = (
    telemetry.join(
        laps,
        (F.col("driver_telemetry") == F.col("driver_lap"))
        & (F.col("session_time") > F.col("start_lap"))
        & (F.col("session_time") < F.col("end_lap")),
        "inner",
    )
    .withColumnRenamed("driver_lap", "driver")
    .groupby("driver", "start_lap", "end_lap")
    .agg(
        *[F.count(F.col("rear_left_brakes_temperature")).alias(f"count")],
        *[
            F.avg(F.col(col)).alias(f"mean_{col}")
            for col in telemetry.columns
            if col not in excluded_columns
        ],
        *[
            F.stddev(F.col(col)).alias(f"stddev_{col}")
            for col in telemetry.columns
            if col not in excluded_columns
        ],
        *[
            F.min(F.col(col)).alias(f"min_{col}")
            for col in telemetry.columns
            if col not in excluded_columns
        ],
        *[
            F.max(F.col(col)).alias(f"max_{col}")
            for col in telemetry.columns
            if col not in excluded_columns
        ],
        *[
            F.expr(f"percentile_approx({col}, 0.25)").alias(f"25th_percentile_{col}")
            for col in telemetry.columns
            if col not in excluded_columns
        ],
        *[
            F.expr(f"percentile_approx({col}, 0.5)").alias(f"50th_percentile_{col}")
            for col in telemetry.columns
            if col not in excluded_columns
        ],
        *[
            F.expr(f"percentile_approx({col}, 0.75)").alias(f"75th_percentile_{col}")
            for col in telemetry.columns
            if col not in excluded_columns
        ],
    )
)

# Process status data with laps
status_with_laps = (
    status.join(
        laps,
        (F.col("driver_telemetry") == F.col("driver_lap"))
        & (F.col("session_time") > F.col("start_lap"))
        & (F.col("session_time") < F.col("end_lap")),
        "inner",
    )
    .withColumnRenamed("driver_lap", "driver")
    .groupby("driver", "start_lap", "end_lap")
    .agg(
        *[
            F.avg(F.col(col)).alias(f"mean_{col}")
            for col in status.columns
            if col not in excluded_columns
        ],
        *[
            F.stddev(F.col(col)).alias(f"stddev_{col}")
            for col in status.columns
            if col not in excluded_columns
        ],
        *[
            F.min(F.col(col)).alias(f"min_{col}")
            for col in status.columns
            if col not in excluded_columns
        ],
        *[
            F.max(F.col(col)).alias(f"max_{col}")
            for col in status.columns
            if col not in excluded_columns
        ],
        *[
            F.expr(f"percentile_approx({col}, 0.25)").alias(f"25th_percentile_{col}")
            for col in status.columns
            if col not in excluded_columns
        ],
        *[
            F.expr(f"percentile_approx({col}, 0.5)").alias(f"50th_percentile_{col}")
            for col in status.columns
            if col not in excluded_columns
        ],
        *[
            F.expr(f"percentile_approx({col}, 0.75)").alias(f"75th_percentile_{col}")
            for col in status.columns
            if col not in excluded_columns
        ],
    )
)

# Process damage data with laps
damage_with_laps = (
    damage.join(
        laps,
        (F.col("driver_telemetry") == F.col("driver_lap"))
        & (F.col("session_time") > F.col("start_lap"))
        & (F.col("session_time") < F.col("end_lap")),
        "inner",
    )
    .withColumnRenamed("driver_lap", "driver")
    .groupby("driver", "start_lap", "end_lap")
    .agg(
        *[
            F.avg(F.col(col)).alias(f"mean_{col}")
            for col in damage.columns
            if col not in excluded_columns
        ],
        *[
            F.stddev(F.col(col)).alias(f"stddev_{col}")
            for col in damage.columns
            if col not in excluded_columns
        ],
        *[
            F.min(F.col(col)).alias(f"min_{col}")
            for col in damage.columns
            if col not in excluded_columns
        ],
        *[
            F.max(F.col(col)).alias(f"max_{col}")
            for col in damage.columns
            if col not in excluded_columns
        ],
        *[
            F.expr(f"percentile_approx({col}, 0.25)").alias(f"25th_percentile_{col}")
            for col in damage.columns
            if col not in excluded_columns
        ],
        *[
            F.expr(f"percentile_approx({col}, 0.5)").alias(f"50th_percentile_{col}")
            for col in damage.columns
            if col not in excluded_columns
        ],
        *[
            F.expr(f"percentile_approx({col}, 0.75)").alias(f"75th_percentile_{col}")
            for col in damage.columns
            if col not in excluded_columns
        ],
    )
)

# Join all processed data into one consolidated DataFrame
consolidated_df = telemetry_with_laps.join(
    status_with_laps, ["driver", "start_lap", "end_lap"], "inner"
).join(damage_with_laps, ["driver", "start_lap", "end_lap"], "inner")

# Save the consolidated DataFrame
consolidated_df.write.mode("overwrite").save("delta/lap_results")
