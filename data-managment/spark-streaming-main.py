from pyspark.sql.session import SparkSession
from pyspark.sql.types import (
    ArrayType,
    MapType,
    FloatType,
    IntegerType,
    StringType,
)
import pyspark.sql.functions as F
from packets import Packet
from track import Track
from delta import *
import pandas as pd
import sys

assert sys.argv.__len__() > 1, "Please provide a valid name for the session"
SESSION_NAME = sys.argv[1]

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
    .withColumn(
        "packet_size", F.udf(lambda x: len(x), IntegerType())(F.col("udp_packet"))
    )
    .withColumn(
        "packet_name",
        F.udf(lambda x: Packet.get_name_by_size(x), StringType())(F.col("packet_size")),
    )
    .withColumn(
        "packet_category",
        F.udf(lambda x: Packet.get_category_by_name(x), IntegerType())(
            F.col("packet_name")
        ),
    )
    .withColumn(
        "packet_decoded",
        F.udf(
            lambda x, y: Packet.extract(Packet.decode(x, y), y),
            ArrayType(MapType(StringType(), FloatType())),
        )(F.col("udp_packet"), F.col("packet_name")),
    )
    .filter(F.col("packet_decoded").isNotNull())
    .withColumn(
        "session_uid",
        F.udf(
            lambda x, y: Packet.get_session_uid(x, y),
            FloatType(),
        )(F.col("udp_packet"), F.col("packet_name")),
    )
    .withColumn(
        "session_time",
        F.udf(
            lambda x, y: Packet.get_session_time(x, y),
            FloatType(),
        )(F.col("udp_packet"), F.col("packet_name")),
    )
    .withColumn("session_type", F.lit(SESSION_NAME))
    .select("*", F.posexplode("packet_decoded").alias("driver", "driver_packet"))
)

participants = (
    ingestion.filter(F.col("packet_name") == "Participants")
    .withColumn(
        "name",
        F.udf(lambda x: Packet.get_driver_name(x["driverId"]), StringType())(
            F.col("driver_packet")
        ),
    )
    .withColumn(
        "team",
        F.udf(lambda x: Packet.get_team_name(x["teamId"]), StringType())(
            F.col("driver_packet")
        ),
    )
    .withColumn(
        "nationality",
        F.udf(lambda x: Packet.get_nationality(x["nationality"]), StringType())(
            F.col("driver_packet")
        ),
    )
    .select(
        "session_type",
        "session_time",
        "driver",
        "name",
        "team",
        "nationality",
    )
    .writeStream.queryName("participants")
    .trigger(once=True)
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/delta/participants/_checkpoints/")
    .start("delta/participants")
)

laps_detection = (
    ingestion.filter(F.col("packet_name") == "Motion")
    .withColumn(
        "position",
        F.udf(
            lambda x: Track.find_closest_value(
                x["world_position_x"],
                x["world_position_y"],
                x["world_position_z"],
            ),
            FloatType(),
        )(F.col("driver_packet")),
    )
    .select("session_type", "session_time", "driver", "position")
    .groupby(F.col("driver"))
    .applyInPandas(
        Track.compare_positions,
        schema="session_type string, driver long, session_time float",
    )
    .writeStream.queryName("laps")
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/delta/laps/_checkpoints/")
    .start("delta/laps")
)

telemetry = (
    ingestion.filter(F.col("packet_name") == "Car Telemetry")
    .withColumn(
        "filtered_packet",
        F.udf(
            lambda x, y: Packet.filter_packet_data(x, y),
            MapType(StringType(), FloatType()),
        )(F.col("driver_packet"), F.col("packet_name")),
    )
    .select("session_type", "session_time", "driver", "filtered_packet")
    .withColumn("keys", F.map_keys(F.col("filtered_packet")))
    .select(
        "*",
        *[
            F.col("filtered_packet").getItem(key).alias(key)
            for key in [
                "speed",
                "throttle",
                "steer",
                "brake",
                "clutch",
                "gear",
                "engine_rpm",
                "drs",
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
    .writeStream.queryName("telemetry")
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/delta/telemetry/_checkpoints/")
    .start("delta/telemetry")
)

status = (
    ingestion.filter(F.col("packet_name") == "Car Status")
    .withColumn(
        "filtered_packet",
        F.udf(
            lambda x, y: Packet.filter_packet_data(x, y),
            MapType(StringType(), FloatType()),
        )(F.col("driver_packet"), F.col("packet_name")),
    )
    .select("session_type", "session_time", "driver", "filtered_packet")
    .withColumn("keys", F.map_keys(F.col("filtered_packet")))
    .select(
        "*",
        *[
            F.col("filtered_packet").getItem(key).alias(key)
            for key in [
                "fuelMix",
                "frontBrakeBias",
                "pitLimiterStatus",
                "fuelInTank",
                "fuelCapacity",
                "fuelRemainingLaps",
                "drsAllowed",
                "drsActivationDistance",
                "ersStoreEnergy",
                "ersDeployMode",
                "ersDeployedThisLap",
                "actualTyreCompound",
            ]
        ],
    )
    .drop("filtered_packet", "keys")
    .writeStream.queryName("status")
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/delta/status/_checkpoints/")
    .start("delta/status")
)

damage = (
    ingestion.filter(F.col("packet_name") == "Car Damage")
    .withColumn(
        "filtered_packet",
        F.udf(
            lambda x, y: Packet.filter_packet_data(x, y),
            MapType(StringType(), FloatType()),
        )(F.col("driver_packet"), F.col("packet_name")),
    )
    .select("session_type", "session_time", "driver", "filtered_packet")
    .withColumn("keys", F.map_keys(F.col("filtered_packet")))
    .select(
        "*",
        *[
            F.col("filtered_packet").getItem(key).alias(key)
            for key in [
                "rear_left_tyresDamage",
                "rear_right_tyresDamage",
                "front_left_tyresDamage",
                "front_right_tyresDamage",
            ]
        ],
    )
    .drop("filtered_packet", "keys")
    .writeStream.queryName("damage")
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/delta/damage/_checkpoints/")
    .start("delta/damage")
)

motion = (
    ingestion.filter(F.col("packet_name") == "Motion")
    .withColumn(
        "filtered_packet",
        F.udf(
            lambda x, y: Packet.filter_packet_data(x, y),
            MapType(StringType(), FloatType()),
        )(F.col("driver_packet"), F.col("packet_name")),
    )
    .select("session_type", "session_time", "driver", "filtered_packet")
    .withColumn("keys", F.map_keys(F.col("filtered_packet")))
    .select(
        "*",
        *[
            F.col("filtered_packet").getItem(key).alias(key)
            for key in [
                "g_force_lateral",
                "g_force_longitudinal",
                "g_force_vertical",
                "yaw",
                "pitch",
                "roll",
            ]
        ],
    )
    .drop("filtered_packet", "keys")
    .writeStream.queryName("motion")
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/delta/motion/_checkpoints/")
    .start("delta/motion")
    .awaitTermination()
)
