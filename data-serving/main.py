from kafka import KafkaConsumer
import websockets
import asyncio
import logging
import socket
import json
import os


async def send_incremental_messages(socket, consumer: KafkaConsumer):
    while True:
        event = next(consumer)
        logging.info(f"Event received: {event}")
        if socket.open:
            _, value = event.key, event.value
            await socket.send(value.decode("utf-8"))


async def handle_connection(socket, _):
    logging.info(f"Client connected!")

    await socket.send(json.dumps({"type": "welcome", "engine_rpm": 1231}))

    await send_incremental_messages(socket, consumer)

    async for message in socket:
        for client in connected_clients:
            if client.open:
                await client.send(message)


async def main(
    websockert_host: str,
    websockert_port: int,
    kafka_host: str,
    kafka_port: int,
    kafka_topic: str,
):
    global connected_clients, consumer

    consumer = KafkaConsumer(
        kafka_topic,
        client_id=str(socket.gethostname()),
        bootstrap_servers=f"{kafka_host}:{kafka_port}",
    )
    logging.info(f"Starting kafka on {kafka_host}:{kafka_port}")
    connected_clients = set()

    async def connection_handler(socket, path):
        connected_clients.add(socket)
        try:
            await handle_connection(socket, path)
        finally:
            connected_clients.remove(socket)

    server = await websockets.serve(
        connection_handler, websockert_host, websockert_port
    )
    logging.info(f"Starting websocket on {websockert_host}:{websockert_port}")
    await server.wait_closed()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    asyncio.run(
        main(
            os.environ.get("WEBSOCKET_HOST"),
            int(os.environ.get("WEBSOCKET_PORT")),
            os.environ.get("KAFKA_HOST"),
            int(os.environ.get("KAFKA_PORT")),
            os.environ.get("KAFKA_TOPIC_SERVING"),
        )
    )
