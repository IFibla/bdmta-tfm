FROM bitnami/spark:3.5.1
LABEL authors="ignasi"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# ENTRYPOINT ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2", "spark-main.py"]