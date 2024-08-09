from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from kafka import KafkaConsumer
from packets import Packet
import logging
import socket
import os


def remove_keys_with_prefix(d, prefix):
    """
    Remove key-value pairs from the dictionary where keys start with the given prefix.

    :param d: Dictionary from which to remove key-value pairs.
    :param prefix: Prefix to match the keys.
    :return: A new dictionary with the specified key-value pairs removed.
    """

    def should_keep(key):
        return not key.startswith(prefix)

    def filter_dict(d):
        return {k: v for k, v in d.items() if should_keep(k)}

    return filter_dict(d)


def main(
    kafka_host: str,
    kafka_port: int,
    kafka_topic: str,
    influxdb_host: str,
    influxdb_port: int,
    influxdb_token: str,
    influxdb_org: str,
    influxdb_bucket: str,
):
    consumer = KafkaConsumer(
        kafka_topic,
        client_id=str(socket.gethostname()),
        bootstrap_servers=f"{kafka_host}:{kafka_port}",
        group_id=kafka_topic,
    )

    dbclient = InfluxDBClient(
        url=f"http://{influxdb_host}:{influxdb_port}",
        token=influxdb_token,
        org=influxdb_org,
    )

    write_api = dbclient.write_api(write_options=SYNCHRONOUS)

    logging.info(f"Kafka server: {kafka_host}:{kafka_port}")
    logging.info(f"InfluxDB server: {influxdb_host}:{influxdb_port}")

    while True:
        event = next(consumer)
        key, udp_packet = event.key, event.value
        logging.info(f"Recived message {key} from Kafka topic {kafka_topic}")

        packet_size = len(udp_packet)
        packet_name = Packet.get_name_by_size(packet_size)
        packet_category = Packet.get_category_by_name(packet_name)
        decoded_packet = Packet.decode(udp_packet, packet_name)

        if packet_category == 0 and decoded_packet is not None:
            cars = Packet.extract(decoded_packet, packet_name)
            for idx, car in enumerate(cars):
                point = (
                    Point(packet_name)
                    .tag(
                        "header_session_time", decoded_packet["header"]["session_time"]
                    )
                    .tag(
                        "header_frame_identifier",
                        decoded_packet["header"]["frame_identifier"],
                    )
                    .tag("car_id", idx)
                )
                for field_key, field_value in car.items():
                    point.field(field_key, field_value)
                write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    main(
        os.environ.get("KAFKA_HOST"),
        int(os.environ.get("KAFKA_PORT")),
        os.environ.get("KAFKA_TOPIC"),
        os.environ.get("INFLUXDB_HOST"),
        int(os.environ.get("INFLUXDB_PORT")),
        os.environ.get("INFLUXDB_TOKEN"),
        os.environ.get("INFLUXDB_ORG"),
        os.environ.get("INFLUXDB_BUCKET_BRONZE"),
    )
