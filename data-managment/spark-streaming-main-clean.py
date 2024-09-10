from pyspark.sql.session import SparkSession
from pyspark.sql.types import ArrayType, MapType, FloatType, IntegerType, StringType
import pyspark.sql.functions as F
from packets import Packet
from track import Track
from delta import *
import pandas as pd
import sys

assert len(sys.argv) > 1, "Please provide a valid name for the session"
SESSION_NAME = sys.argv[1]

pd.options.mode.chained_assignment = None

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


def create_ingestion_stream():
    """
    Creates the base ingestion stream from Kafka and applies initial transformations.

    Returns:
    -------
    DataFrame
        The transformed base ingestion DataFrame.
    """
    return (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("subscribe", "stream-ingestion")
        .option("failOnDataLoss", "false")
        .load()
        .selectExpr("value as udp_packet")
        .withColumn(
            "packet_size", F.udf(lambda x: len(x), IntegerType())(F.col("udp_packet"))
        )
        .withColumn(
            "packet_name",
            F.udf(lambda x: Packet.get_name_by_size(x), StringType())(
                F.col("packet_size")
            ),
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
            F.udf(lambda x, y: Packet.get_session_uid(x, y), FloatType())(
                F.col("udp_packet"),
                F.col("packet_name"),
            ),
        )
        .withColumn(
            "session_time",
            F.udf(lambda x, y: Packet.get_session_time(x, y), FloatType())(
                F.col("udp_packet"),
                F.col("packet_name"),
            ),
        )
        .withColumn("session_type", F.lit(SESSION_NAME))
        .select("*", F.posexplode("packet_decoded").alias("driver", "driver_packet"))
    )


def write_stream(df, query_name, output_path, checkpoint_path):
    """
    Writes a DataFrame stream to a Delta table.

    Parameters:
    ----------
    df : DataFrame
        The DataFrame to write.
    query_name : str
        The name of the query for monitoring purposes.
    output_path : str
        The path to write the Delta table data.
    checkpoint_path : str
        The path to store checkpoint data.
    """
    df.writeStream.queryName(query_name).format("delta").outputMode("append").option(
        "checkpointLocation", checkpoint_path
    ).start(output_path)


def process_packet(df, packet_name, columns, query_name, output_path):
    """
    Processes specific packets, applying filtering and transformation based on packet type.

    Parameters:
    ----------
    df : DataFrame
        The base ingestion DataFrame.
    packet_name : str
        The name of the packet to filter and process.
    columns : list of str
        The columns to extract from the filtered packet.
    query_name : str
        The name of the query for the streaming job.
    output_path : str
        The output path for the Delta table.
    """
    filtered_df = (
        df.filter(F.col("packet_name") == packet_name)
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
            *[F.col("filtered_packet").getItem(key).alias(key) for key in columns],
        )
        .drop("filtered_packet", "keys")
    )
    write_stream(
        filtered_df, query_name, output_path, f"/tmp/delta/{query_name}/_checkpoints/"
    )


ingestion = create_ingestion_stream()

# Process Participants Data
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
        F.udf(
            lambda x: Packet.get_nationality(x["nationality"]),
            StringType(),
        )(F.col("driver_packet")),
    )
    .select(
        "session_type",
        "session_time",
        "driver",
        "name",
        "team",
        "nationality",
    )
)

write_stream(
    participants,
    "participants",
    "delta/participants",
    "/tmp/delta/participants/_checkpoints/",
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
        Track.compare_positions_to_extract_laps,
        schema="session_type string, driver long, session_time float",
    )
)

write_stream(laps_detection, "laps", "delta/laps", "/tmp/delta/laps/_checkpoints/")

segments_detection = (
    ingestion.filter(F.col("packet_name") == "Motion")
    .withColumn(
        "segment",
        F.udf(
            lambda x: Track.get_point_category(
                x["world_position_x"], x["world_position_y"], x["world_position_z"]
            ),
            FloatType(),
        )(F.col("driver_packet")),
    )
    .select("session_type", "session_time", "driver", "segment")
    .groupby(F.col("driver"))
    .applyInPandas(
        Track.compare_positions_to_extract_segments,
        schema="session_type string, driver long, session_time float, prev_segment float, segment float",
    )
)

write_stream(
    segments_detection,
    "segments",
    "delta/segments",
    "/tmp/delta/segments/_checkpoints/",
)


# Process Telemetry
process_packet(
    ingestion,
    "Car Telemetry",
    [
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
    ],
    "telemetry",
    "delta/telemetry",
)

# Process Car Status
process_packet(
    ingestion,
    "Car Status",
    [
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
    ],
    "status",
    "delta/status",
)

# Process Car Damage
process_packet(
    ingestion,
    "Car Damage",
    [
        "rear_left_tyresDamage",
        "rear_right_tyresDamage",
        "front_left_tyresDamage",
        "front_right_tyresDamage",
    ],
    "damage",
    "delta/damage",
)

# Process Motion Data
process_packet(
    ingestion,
    "Motion",
    [
        "g_force_lateral",
        "g_force_longitudinal",
        "g_force_vertical",
        "yaw",
        "pitch",
        "roll",
    ],
    "motion",
    "delta/motion",
)

# Await termination of all streams
spark.streams.awaitAnyTermination()
