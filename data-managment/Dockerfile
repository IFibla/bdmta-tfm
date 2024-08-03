FROM bitnami/spark:3.5.1
LABEL authors="ignasi"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# ENTRYPOINT ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,io.delta:delta-spark_2.12:3.2.0", "main.py"]