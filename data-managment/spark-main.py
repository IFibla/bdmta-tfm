from pyspark.sql.types import ArrayType, MapType, FloatType, IntegerType, StringType
from pyspark.sql.functions import col, posexplode, udf
from pyspark.sql.session import SparkSession
from packets import Packet

## --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,io.delta:delta-spark_2.12:3.2.0

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
    .filter(col("packet_category") == 0)
    .withColumn(
        "packet_decoded",
        udf(
            lambda x, y: Packet.extract(Packet.decode(x, y), y),
            ArrayType(MapType(StringType(), FloatType())),
        )(col("udp_packet"), col("packet_name")),
    )
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
    .select("*", posexplode("packet_decoded").alias("driver", "packet_decoded"))
    .writeStream.format("console")
    .start()
    .awaitTermination()
)

# drivers_related = (
#     stream_classification.filter(col("packet_category") == 0)
#     .withColumn(
#         "list_data",
#         udf(lambda x, y: Packet.extract(x, y), ArrayType())(
#             col("decoded_packet"), col("packet_name")
#         ),
#     )
#     .withColumn("expanded_data", explode(col("list_data")))
#     .writeStream.format("console")
#     # .writeStream.foreach(InfluxDBWriter())
#     .start()
#     .awaitTermination()
# )
