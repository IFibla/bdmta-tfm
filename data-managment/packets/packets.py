from ctypes import Structure
from enum import Enum
from .models import *


class Packet(Enum):
    MOTION = (0, "Motion", 1464, 0, PacketMotion, CarMotionData)
    SESSION = (1, "Session", 632, 1, PacketSession, None)
    LAP_DATA = (2, "Lap Data", 972, 0, PacketLap, None)
    EVENT = (3, "Event", 40, 2, None, None)
    PARTICIPANTS = (4, "Participants", 1257, -1, None, None)
    CAR_SETUPS = (5, "Car Setups", 1102, 0, PacketSetups, None)
    CAR_TELEMETRY = (6, "Car Telemetry", 1347, 0, PacketCarTelemetry, CarTelemetryData)
    CAR_STATUS = (7, "Car Status", 1058, 0, PacketCarStatus, CarStatusData)
    FINAL_CLASSIFICATION = (
        8,
        "Final Classification",
        1015,
        0,
        PacketFinalClassification,
        None,
    )
    LOBBY_INFO = (9, "Lobby Info", 1191, 0, None, None)
    CAR_DAMAGE = (10, "Car Damage", 948, 0, PacketCarDamage, CarDamageData)
    SESSION_HISTORY = (11, "Session History", 1155, 3, None, None)

    def __init__(
        self,
        id: int,
        name: str,
        size: int,
        category: int,
        model: Structure,
        inner_model: Structure,
    ):
        self._id = id
        self._name = name
        self._size = size
        self._category = category
        self._model = model
        self._inner_model = inner_model

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        return self._size

    @property
    def category(self) -> int:
        return self._category

    @property
    def model(self) -> Structure:
        return self._model

    @property
    def inner_model(self) -> Structure:
        return self._inner_model

    @classmethod
    def get_name_by_size(cls, size: int) -> str:
        for packet in cls:
            if packet.size == size:
                return packet.name
        return None

    @classmethod
    def get_category_by_name(cls, name: str) -> int:
        for packet in cls:
            if packet.name == name:
                return packet.category
        return None

    @classmethod
    def decode(cls, udp_packet: bytes, name: str) -> dict:
        for packet in cls:
            if packet.name == name and packet.model is not None:
                return packet.model.from_buffer_copy(udp_packet).to_dict()
        return None

    @classmethod
    def extract(cls, decoded_packet: dict, name: str) -> [dict]:
        for packet in cls:
            if packet.name == name and packet.inner_model is not None:
                return decoded_packet[packet.model.ARRAY_NAME]
        return None

    @classmethod
    def flatten(cls, d: dict, parent_key="", sep="_") -> dict:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(cls.flatten(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, (dict, list)):
                        items.extend(
                            cls.flatten(item, f"{new_key}_{i}", sep=sep).items()
                        )
                    else:
                        items.append((f"{new_key}_{i}", item))
            else:
                items.append((new_key, v))
        return dict(items)

    @classmethod
    def get_session_uid(cls, udp_packet: bytes, name: str) -> float:
        for packet in cls:
            if packet.name == name and packet.model is not None:
                return packet.model.from_buffer_copy(udp_packet).to_dict()["header"][
                    "session_uid"
                ]
        return None

    @classmethod
    def get_session_time(cls, udp_packet: bytes, name: str) -> float:
        for packet in cls:
            if packet.name == name and packet.model is not None:
                return packet.model.from_buffer_copy(udp_packet).to_dict()["header"][
                    "session_time"
                ]
        return None

    @classmethod
    def filter_speed_layer_data(
        cls, packet_dict: dict[str, float], name: str
    ) -> dict[str, float]:
        for packet in cls:
            if packet.name == name and packet.inner_model is not None:
                return packet.inner_model.speed_layer_filter(packet_dict)
        return None

    @classmethod
    def filter_silver_layer_data(cls) -> [str]:
        result = []
        for packet in cls:
            if packet.inner_model is not None:
                result.extend(packet.inner_model.get_silver_layer_data())
        return result
