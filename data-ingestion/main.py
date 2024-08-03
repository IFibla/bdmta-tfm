from kafka import KafkaProducer
import logging
import socket
import time
import uuid
import os

def main(
    socket_host: str,
    socket_port: int,
    socket_maxsize: int,
    kafka_host: str,
    kafka_port: int,
    kafka_topic: str,
):
    """
    Start a UDP server to receive data and send it to Kafka.

    Args:
    - socket_host (str): Hostname/IP on which the UDP server will bind.
    - socket_port (int): Port on which the UDP server will listen.
    - socket_maxsize (int): Maximum size of UDP packets to receive.
    - kafka_host (str): Kafka broker hostname/IP.
    - kafka_port (int): Kafka broker port.
    - kafka_topic (str): Kafka topic to which data will be sent.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((socket_host, socket_port))

    producer = KafkaProducer(
        bootstrap_servers=f"{kafka_host}:{kafka_port}",
        client_id=str(socket.gethostname()),
    )

    logging.info(f"UDP server listening on {socket_host}:{socket_port}...")
    logging.info(f"Kafka server: {kafka_host}:{kafka_port}")

    while True:
        key = str(uuid.uuid4()).encode()
        # value, _ = server_socket.recvfrom(socket_maxsize)
        producer.send(kafka_topic, key=key, value=key)
        logging.info(f"Sent message {key} to Kafka topic {kafka_topic}")
        time.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    main(
        os.environ.get("SOCKET_HOST"),
        int(os.environ.get("SOCKET_PORT")),
        int(os.environ.get("SOCKET_MAXSIZE")),
        os.environ.get("KAFKA_HOST"),
        int(os.environ.get("KAFKA_PORT")),
        os.environ.get("KAFKA_TOPIC")
    )
