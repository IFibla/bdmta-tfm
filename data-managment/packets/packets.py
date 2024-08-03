from ctypes import Structure
from enum import Enum
from models import *


class Packet(Enum):
    MOTION = (0, "Motion", 1464, 0, PacketMotion)
    SESSION = (1, "Session", 632, 1, PacketSession)
    LAP_DATA = (2, "Lap Data", 972, 0, PacketLap)
    EVENT = (3, "Event", 40, 2, None)
    PARTICIPANTS = (4, "Participants", 1257, 0, PacketParticipants)
    CAR_SETUPS = (5, "Car Setups", 1102, 0, PacketSetups)
    CAR_TELEMETRY = (6, "Car Telemetry", 1347, 0, PacketCarTelemetry)
    CAR_STATUS = (7, "Car Status", 1058, 0, PacketCarStatus)
    FINAL_CLASSIFICATION = (8, "Final Classification", 1015, 0, PacketFinalClassification)
    LOBBY_INFO = (9, "Lobby Info", 1191, 0, None)
    CAR_DAMAGE = (10, "Car Damage", 948, 0, PacketCarDamage)
    SESSION_HISTORY = (11, "Session History", 1155, 3, None)

    MAX_MARSHALL_ZONES = 21
    MAX_NUMBER_OF_PARTICIPANTS = 22
    MAX_WEATHER_FORECAST_SAMPLES = 56

    def __init__(self, id: int, name: str, size: int, category: int, model: Structure):
        self._id = id
        self._name = name
        self._size = size
        self._category = category
        self._model = model

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

    @classmethod
    def get_name_by_size(cls, size: int) -> str:
        for packet in cls:
            if packet.size == size:
                return packet.name
        raise ValueError(f"No packet found with size {size}")

    @classmethod
    def get_category_by_name(cls, name: str) -> int:
        for packet in cls:
            if packet.name == name:
                return packet.category
        raise ValueError(f"No packet found with name {name}")

    @classmethod
    def decode(cls, udp_packet: bytes, name: str) -> dict:
        for packet in cls:
            if packet.name == name:
                return packet.model.from_buffer_copy(udp_packet).to_dict()
        raise ValueError(f"No packet found with name {name}")

    @classmethod
    def extract(cls, decoded_packet: dict, name: str) -> [dict]:
        for packet in cls:
            if packet.name == name:
                return decoded_packet[packet.model.ARRAY_NAME]
        raise ValueError(f"No packet found with name {name}")
