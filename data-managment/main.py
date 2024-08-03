from pyspark.sql.types import ArrayType, IntegerType, StringType
from pyspark.sql.functions import col, explode, udf
from pyspark.sql.session import SparkSession
from packets import Packet
from delta import *

## --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,io.delta:delta-spark_2.12:3.2.0

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

raw_to_bronze = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", f"kafka:9092")
    .option("subscribe", "stream-ingestion")
    .load()
    .selectExpr("CAST(value AS STRING) as udp_packet")
    .withColumn(
        "packet_name",
        udf(lambda x: Packet.get_name_by_size(len(x)), StringType())(col("udp_packet")),
    )
    .withColumn(
        "packet_category",
        udf(lambda x: Packet.get_category_by_name(x), IntegerType())(
            col("packet_name")
        ),
    )
    .withColumn(
        "decoded_packet",
        udf(lambda x, y: Packet.decode(x, y), StringType())(
            col("udp_packet"), col("packet_name")
        ),
    )
)

(
    raw_to_bronze.writeStream.format("delta")
    .option("checkpointLocation", "/tmp/checkpoint")
    .partitionBy("packet_category")
    .start("/tmp/bronze-delta-table")
)

speed_layer = (
    raw_to_bronze.filter(col("packet_category") == 0)
    .withColumn(
        "list_data",
        udf(lambda x, y: Packet.extract(x, y), ArrayType())(
            col("decoded_packet"), col("packet_name")
        ),
    )
    .withColumn("expanded_data", explode(col("list_data")))
)
