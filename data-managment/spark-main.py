from pyspark.sql.streaming.state import GroupStateTimeout, GroupState
from pyspark.sql.types import (
    ArrayType,
    MapType,
    FloatType,
    IntegerType,
    StringType,
    StructType,
    StructField,
    DoubleType,
)
from pyspark.sql.functions import (
    col,
    collect_list,
    posexplode,
    to_json,
    lag,
    struct,
    sum as spark_sum,
    udf,
    when,
    lit,
    size,
    coalesce,
    row_number,
)
from pyspark.sql.session import SparkSession
from packets import Packet
from track import Track
from delta import *
import pandas as pd

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

ingest_decode_explode = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", f"kafka:9092")
    .option("subscribe", "stream-ingestion")
    .load()
    .selectExpr("value as udp_packet")
    .withColumn("packet_size", udf(lambda x: len(x), IntegerType())(col("udp_packet")))
    .withColumn(
        "packet_name",
        udf(lambda x: Packet.get_name_by_size(x), StringType())(col("packet_size")),
    )
    .withColumn(
        "packet_category",
        udf(lambda x: Packet.get_category_by_name(x), IntegerType())(
            col("packet_name")
        ),
    )
    .withColumn(
        "packet_decoded",
        udf(
            lambda x, y: Packet.extract(Packet.decode(x, y), y),
            ArrayType(MapType(StringType(), FloatType())),
        )(col("udp_packet"), col("packet_name")),
    )
    .filter(col("packet_decoded").isNotNull())
    .withColumn(
        "session_uid",
        udf(
            lambda x, y: Packet.get_session_uid(x, y),
            FloatType(),
        )(col("udp_packet"), col("packet_name")),
    )
    .withColumn(
        "session_time",
        udf(
            lambda x, y: Packet.get_session_time(x, y),
            FloatType(),
        )(col("udp_packet"), col("packet_name")),
    )
    .select("*", posexplode("packet_decoded").alias("driver", "driver_packet"))
    .withColumn(
        "driver_packet",
        udf(
            lambda x: (
                {
                    **x,
                    "world_position_perc": Track.find_closest_value(
                        x["world_position_x"],
                        x["world_position_y"],
                        x["world_position_z"],
                    ),
                }
                if "world_position_x" in x
                else x
            ),
            MapType(StringType(), FloatType()),
        )(col("driver_packet")),
    )
)

speed_layer = (
    ingest_decode_explode.withColumn(
        "filtered_packet",
        udf(
            lambda x, y: Packet.filter_speed_layer_data(x, y),
            MapType(StringType(), FloatType()),
        )(col("driver_packet"), col("packet_name")),
    )
    .filter(col("filtered_packet").isNotNull())
    .filter(col("driver") == 0)
    .select("driver", "packet_name", "filtered_packet")
    .select(to_json(struct("driver", "packet_name", "filtered_packet")).alias("value"))
    # .writeStream.format("kafka")
    # .option("kafka.bootstrap.servers", f"kafka:9092")
    # .option("topic", "stream-serving")
    # .option("checkpointLocation", "/tmp/checkpoint")  # Ensure this path is accessible
    # .start()
    # .awaitTermination()
)

output_schema = StructType(
    [
        StructField("driver", IntegerType(), True),
        StructField("session_time", FloatType(), True),
        StructField("position", FloatType(), True),
        StructField("lap", IntegerType(), True),
    ]
)


def rewrite_df(generator, lap):
    rows = pd.concat(generator, ignore_index=True)
    rows.sort_values(by=["session_time"], inplace=True)

    if not any(rows["lap"] != -1):
        rows.iloc[0, rows.columns.get_loc("lap")] = lap

    for i in range(1, len(rows)):
        if rows.iloc[i].position == -1:
            rows.iloc[i, rows.columns.get_loc("lap")] = lap
            rows.iloc[i, rows.columns.get_loc("position")] = rows.iloc[i - 1].position
        elif rows.iloc[i - 1].position > rows.iloc[i].position:
            lap += 1
            rows.iloc[i, rows.columns.get_loc("lap")] = lap
        else:
            rows.iloc[i, rows.columns.get_loc("lap")] = lap

    return rows, lap


def add_laps(key, pdf_iter, state):
    current_lap = state.get[0] if state.exists else 1
    pdf_iter, lap = rewrite_df(pdf_iter, current_lap)
    state.update((lap,))
    yield pdf_iter


df_with_position = (
    ingest_decode_explode.withColumn(
        "position",
        udf(
            lambda x: x["world_position_perc"] if "world_position_perc" in x else None,
            FloatType(),
        )(col("driver_packet")),
    )
    .fillna(-1, subset=["position"])
    .withColumn("lap", lit(-1))
    .select(
        col("driver"),
        col("session_time"),
        col("lap"),
        col("position"),
    )
    .filter(col("driver") == 0)
    .groupby("driver")
    .applyInPandasWithState(
        add_laps,
        outputStructType=output_schema,
        stateStructType="current_lap int",
        outputMode="Update",
        timeoutConf=GroupStateTimeout.NoTimeout,
    )
    .writeStream.format("console")
    .outputMode("update")
    .start()
    .awaitTermination()
)
