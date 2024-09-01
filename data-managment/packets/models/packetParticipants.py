from ctypes import Structure, c_char, c_uint8, c_uint16
from .packetHeader import PacketHeader

MAX_MARSHALL_ZONES = 21
MAX_NUMBER_OF_PARTICIPANTS = 22
MAX_WEATHER_FORECAST_SAMPLES = 56


class ParticipantData(Structure):
    _pack_ = 1

    _fields_ = [
        ("aiControlled", c_uint8),
        ("driverId", c_uint8),
        ("networkId", c_uint8),
        ("teamId", c_uint8),
        ("myTeam", c_uint8),
        ("raceNumber", c_uint8),
        ("nationality", c_uint8),
        ("name", c_char * 48),
        ("yourTelemetry", c_uint8),
    ]

    def to_dict(self):
        return {
            "driverId": float(self.driverId),
            "teamId": float(self.teamId),
            "nationality": float(self.nationality),
        }


class PacketParticipants(Structure):
    ARRAY_NAME = "participants"

    _pack_ = 1

    _fields_ = [
        ("header", PacketHeader),
        ("numActiveCars", c_uint8),
        ("participants", ParticipantData * MAX_NUMBER_OF_PARTICIPANTS),
    ]

    def to_dict(self):
        return {
            "header": self.header.to_dict(),
            self.ARRAY_NAME: [
                self.participants[i].to_dict()
                for i in range(MAX_NUMBER_OF_PARTICIPANTS)
            ],
            "numActiveCars": self.numActiveCars,
        }
