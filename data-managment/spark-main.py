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

bronze = (
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
    bronze.withColumn(
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
        StructField("timestamp", TimestampType(), True),
        StructField("driver", IntegerType(), True),
        StructField("session_time", FloatType(), True),
        StructField("position", FloatType(), True),
        StructField("lap", IntegerType(), True),
    ]
    + [StructField(var, FloatType(), True) for var in Packet.filter_silver_layer_data()]
)


bronze_to_silver = bronze.withColumn(
    "position",
    udf(
        lambda x: x["world_position_perc"] if "world_position_perc" in x else None,
        FloatType(),
    )(col("driver_packet")),
)

for var in Packet.filter_silver_layer_data():
    bronze_to_silver = bronze_to_silver.withColumn(
        var,
        udf(
            lambda x: x[var] if var in x else None,
            FloatType(),
        )(col("driver_packet")),
    )

silver = (
    bronze_to_silver.fillna(-1, subset=["position"])
    .withColumn("lap", lit(-1))
    .drop(
        col("udp_packet"),
        col("packet_size"),
        col("packet_name"),
        col("packet_category"),
        col("packet_decoded"),
        col("session_uid"),
        col("driver_packet"),
    )
    .withWatermark("timestamp", "1 minute")
    .groupby("driver")
    .applyInPandasWithState(
        Track.add_laps,
        outputStructType=output_schema,
        stateStructType="current_lap int",
        outputMode="Append",
        timeoutConf=GroupStateTimeout.ProcessingTimeTimeout,
    )
    .drop(col("position"), col("session_time"))
    .writeStream.format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/delta/_checkpoints/")
    .start("delta/events")
    .awaitTermination()
)

# gold = (
#     silver.groupby(col("driver"), col("lap"))
#     .agg(
#         *[
#             F.count(F.col(col)).alias(f"count_{col}")
#             for col in Packet.filter_silver_layer_data()
#         ],
#         *[
#             F.avg(F.col(col)).alias(f"mean_{col}")
#             for col in Packet.filter_silver_layer_data()
#         ],
#         *[
#             F.stddev(F.col(col)).alias(f"stddev_{col}")
#             for col in Packet.filter_silver_layer_data()
#         ],
#         *[
#             F.min(F.col(col)).alias(f"min_{col}")
#             for col in Packet.filter_silver_layer_data()
#         ],
#         *[
#             F.max(F.col(col)).alias(f"max_{col}")
#             for col in Packet.filter_silver_layer_data()
#         ],
#         *[
#             F.expr(f"percentile_approx({col}, 0.25)").alias(f"25th_percentile_{col}")
#             for col in Packet.filter_silver_layer_data()
#         ],
#         *[
#             F.expr(f"percentile_approx({col}, 0.5)").alias(f"50th_percentile_{col}")
#             for col in Packet.filter_silver_layer_data()
#         ],
#         *[
#             F.expr(f"percentile_approx({col}, 0.75)").alias(f"75th_percentile_{col}")
#             for col in Packet.filter_silver_layer_data()
#         ],
#     )
#     .select("driver", "lap")
#     .writeStream.outputMode("update")
#     .format("console")
#     # .format("csv")
#     # .option("header", "true")
#     # .option("path", "gold")
#     # .option("checkpointLocation", "/tmp/checkpoint")
#     .start()
#     .awaitTermination()
# )
