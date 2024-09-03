from ctypes import Structure
from .constants import *
from enum import Enum
from .models import *


class Packet(Enum):
    """
    An enumeration class that represents various data packets used in telemetry.

    Each packet type is defined with specific attributes including an identifier, name,
    data size, category, and associated data models. The class provides methods to decode,
    extract, and manipulate packet data for various telemetry purposes.
    """

    MOTION = (0, "Motion", 1464, 0, PacketMotion, CarMotionData)
    SESSION = (1, "Session", 632, 1, PacketSession, None)
    LAP_DATA = (2, "Lap Data", 972, 0, PacketLap, None)
    EVENT = (3, "Event", 40, 2, None, None)
    PARTICIPANTS = (4, "Participants", 1257, 2, PacketParticipants, ParticipantData)
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
        """
        Initializes a Packet instance.

        Parameters:
        ----------
        id : int
            The unique identifier for the packet type.
        name : str
            The name of the packet.
        size : int
            The size of the packet in bytes.
        category : int
            The category identifier of the packet.
        model : Structure
            The primary data model associated with the packet.
        inner_model : Structure
            The inner data model associated with the packet.
        """
        self._id = id
        self._name = name
        self._size = size
        self._category = category
        self._model = model
        self._inner_model = inner_model

    @property
    def name(self) -> str:
        """Returns the name of the packet."""
        return self._name

    @property
    def size(self) -> int:
        """Returns the size of the packet in bytes."""
        return self._size

    @property
    def category(self) -> int:
        """Returns the category identifier of the packet."""
        return self._category

    @property
    def model(self) -> Structure:
        """Returns the data model associated with the packet."""
        return self._model

    @property
    def inner_model(self) -> Structure:
        """Returns the inner data model associated with the packet."""
        return self._inner_model

    @classmethod
    def get_name_by_size(cls, size: int) -> str:
        """
        Retrieves the name of a packet based on its size.

        Parameters:
        ----------
        size : int
            The size of the packet in bytes.

        Returns:
        -------
        str
            The name of the packet with the given size, or None if not found.
        """
        for packet in cls:
            if packet.size == size:
                return packet.name
        return None

    @classmethod
    def get_category_by_name(cls, name: str) -> int:
        """
        Retrieves the category of a packet based on its name.

        Parameters:
        ----------
        name : str
            The name of the packet.

        Returns:
        -------
        int
            The category of the packet, or None if not found.
        """
        for packet in cls:
            if packet.name == name:
                return packet.category
        return None

    @classmethod
    def decode(cls, udp_packet: bytes, name: str) -> dict:
        """
        Decodes a UDP packet based on its name and associated model.

        Parameters:
        ----------
        udp_packet : bytes
            The raw UDP packet data.
        name : str
            The name of the packet type to decode.

        Returns:
        -------
        dict
            A dictionary representing the decoded packet data, or None if decoding fails.
        """
        for packet in cls:
            if packet.name == name and packet.model is not None:
                return packet.model.from_buffer_copy(udp_packet).to_dict()
        return None

    @classmethod
    def extract(cls, decoded_packet: dict, name: str) -> [dict]:
        """
        Extracts inner model data from a decoded packet.

        Parameters:
        ----------
        decoded_packet : dict
            The decoded packet data.
        name : str
            The name of the packet type to extract data from.

        Returns:
        -------
        list[dict]
            A list of dictionaries representing extracted data, or None if extraction fails.
        """
        for packet in cls:
            if packet.name == name and packet.inner_model is not None:
                return decoded_packet[packet.model.ARRAY_NAME]
        return None

    @classmethod
    def flatten(cls, d: dict, parent_key: str = "", sep: str = "_") -> dict:
        """
        Flattens a nested dictionary into a single-level dictionary.

        Parameters:
        ----------
        d : dict
            The dictionary to flatten.
        parent_key : str, optional
            The base key for the flattened entries, default is an empty string.
        sep : str, optional
            Separator used between parent and child keys, default is '_'.

        Returns:
        -------
        dict
            The flattened dictionary.
        """
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
        """
        Retrieves the session UID from a packet header.

        Parameters:
        ----------
        udp_packet : bytes
            The raw UDP packet data.
        name : str
            The name of the packet type to decode.

        Returns:
        -------
        float
            The session UID, or None if not found.
        """
        for packet in cls:
            if packet.name == name and packet.model is not None:
                return packet.model.from_buffer_copy(udp_packet).to_dict()["header"][
                    "session_uid"
                ]
        return None

    @classmethod
    def get_session_time(cls, udp_packet: bytes, name: str) -> float:
        """
        Retrieves the session time from a packet header.

        Parameters:
        ----------
        udp_packet : bytes
            The raw UDP packet data.
        name : str
            The name of the packet type to decode.

        Returns:
        -------
        float
            The session time, or None if not found.
        """
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
        """
        Filters data based on speed layer criteria.

        Parameters:
        ----------
        packet_dict : dict[str, float]
            The packet data dictionary to filter.
        name : str
            The name of the packet type for filtering.

        Returns:
        -------
        dict[str, float]
            The filtered data, or None if filtering fails.
        """
        for packet in cls:
            if packet.name == name and packet.inner_model is not None:
                return packet.inner_model.speed_layer_filter(packet_dict)
        return None

    @classmethod
    def filter_packet_data(
        cls, packet_dict: dict[str, float], name: str
    ) -> dict[str, float]:
        """
        Filters data based on silver layer criteria.

        Parameters:
        ----------
        packet_dict : dict[str, float]
            The packet data dictionary to filter.
        name : str
            The name of the packet type for filtering.

        Returns:
        -------
        dict[str, float]
            The filtered data, or None if filtering fails.
        """
        for packet in cls:
            if packet.name == name and packet.inner_model is not None:
                return packet.inner_model.get_silver_layer_data(packet_dict)
        return None

    @staticmethod
    def get_driver_name(driver_id: int) -> str:
        """
        Returns the driver's name based on their ID.

        Parameters:
        ----------
        driver_id : int
            The ID of the driver.

        Returns:
        -------
        str
            The name of the driver.
        """
        return DRIVER_NAMES[driver_id]

    @staticmethod
    def get_team_name(team_id: int) -> str:
        """
        Returns the team name based on its ID.

        Parameters:
        ----------
        team_id : int
            The ID of the team.

        Returns:
        -------
        str
            The name of the team.
        """
        return TEAMS_NAMES[team_id]

    @staticmethod
    def get_nationality(nationality_id: int) -> str:
        """
        Returns the nationality based on its ID.

        Parameters:
        ----------
        nationality_id : int
            The ID of the nationality.

        Returns:
        -------
        str
            The name of the nationality.
        """
        return NATIONALITY_NAMES[nationality_id]
