from pyspark.sql import Window
from pyspark.sql.streaming.state import GroupStateTimeout, GroupState
from pyspark.sql.types import (
    ArrayType,
    MapType,
    FloatType,
    IntegerType,
    StringType,
    StructType,
    StructField,
    TimestampType,
)
from pyspark.sql.functions import (
    col,
    posexplode,
    to_json,
    struct,
    udf,
    lit,
)
import pyspark.sql.functions as F
from pyspark.sql.session import SparkSession
from packets import Packet
from track import Track
from delta import *
import pandas as pd
import json

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

ingestion = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", f"kafka:9092")
    .option("subscribe", "stream-ingestion")
    .option("failOnDataLoss", "false")
    .load()
    .selectExpr("value as udp_packet")
    .withColumn("timestamp", F.current_timestamp())
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
)

participants = (
    ingestion.filter(col("packet_name") == "Participants")
    .withColumn(
        "name",
        udf(lambda x: Packet.get_driver_name(x["driverId"]), StringType())(
            col("driver_packet")
        ),
    )
    .withColumn(
        "team",
        udf(lambda x: Packet.get_team_name(x["teamId"]), StringType())(
            col("driver_packet")
        ),
    )
    .withColumn(
        "nationality",
        udf(lambda x: Packet.get_nationality(x["nationality"]), StringType())(
            col("driver_packet")
        ),
    )
    .select(
        "driver",
        "name",
        "team",
        "nationality",
    )
    .writeStream.format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/delta/participants/_checkpoints/")
    .start("delta/participants")
)

laps_detection = (
    ingestion.filter(col("packet_name") == "Motion")
    .withColumn(
        "position",
        udf(
            lambda x: Track.find_closest_value(
                x["world_position_x"],
                x["world_position_y"],
                x["world_position_z"],
            ),
            FloatType(),
        )(col("driver_packet")),
    )
    .select("driver", "session_time", "position")
    .groupby(col("driver"))
    .applyInPandas(
        Track.compare_positions,
        schema="driver long, session_time float",
    )
    .writeStream.format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/delta/laps/_checkpoints/")
    .start("delta/laps")
)

telemetry = (
    ingestion.filter(col("packet_name") == "Car Telemetry")
    .withColumn(
        "filtered_packet",
        udf(
            lambda x, y: Packet.filter_silver_layer_data(x, y),
            MapType(StringType(), FloatType()),
        )(col("driver_packet"), col("packet_name")),
    )
    .select("driver", "filtered_packet", "session_time")
    .withColumn("keys", F.map_keys(col("filtered_packet")))
    .select(
        "*",
        *[
            col("filtered_packet").getItem(key).alias(key)
            for key in [
                "rear_left_brakes_temperature",
                "rear_right_brakes_temperature",
                "front_left_brakes_temperature",
                "front_right_brakes_temperature",
                "rear_left_tyres_surface_temperature",
                "rear_right_tyres_surface_temperature",
                "front_left_tyres_surface_temperature",
                "front_right_tyres_surface_temperature",
                "rear_left_tyres_inner_temperature",
                "rear_right_tyres_inner_temperature",
                "front_left_tyres_inner_temperature",
                "front_right_tyres_inner_temperature",
                "engine_temperature",
                "rear_left_tyres_pressure",
                "rear_right_tyres_pressure",
                "front_left_tyres_pressure",
                "front_right_tyres_pressure",
            ]
        ],
    )
    .drop("filtered_packet", "keys")
    .writeStream.format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/delta/telemetry/_checkpoints/")
    .start("delta/telemetry")
)


def process_and_update_laps(batch_df, epoch_id):
    window_spec = Window.partitionBy("driver").orderBy("session_time")

    batch_df.withColumn(
        "prev_session_time", F.lag("session_time", 1).over(window_spec)
    ).filter(col("prev_session_time").isNotNull()).write.format("delta").mode(
        "append"
    ).save(
        "delta/laps_updated"
    )


participants_df = spark.read.format("delta").load("delta/participants").dropDuplicates()

query = (
    spark.readStream.format("delta")
    .load("delta/laps")
    .join(participants_df, on="driver", how="inner")
    .writeStream.trigger(processingTime="30 seconds")
    .foreachBatch(process_and_update_laps)
    # .format("console")
    .option("checkpointLocation", "/tmp/delta/laps_updated/_checkpoints/")
    .start()
    .awaitTermination()
)
