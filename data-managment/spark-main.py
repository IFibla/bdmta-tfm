from pyspark.sql.types import ArrayType, MapType, FloatType, IntegerType, StringType
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
)
from pyspark.sql.session import SparkSession
from packets import Packet
from track import Track

## --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2

spark = (
    SparkSession.builder.appName("DataDash")
    .config("spark.sql.adaptive.enabled", True)
    .getOrCreate()
)
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
    .writeStream.format("console")
    .outputMode("update")
    .start()
    .awaitTermination()
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

batch_layer = ingest_decode_explode.groupby("driver").agg(collect_list("driver_packet"))
