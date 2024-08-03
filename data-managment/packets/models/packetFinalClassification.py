from ctypes import Structure, c_uint8, c_uint32, c_double
from .packetHeader import PacketHeader
from ..packets import Packet


class FinalClassificationData(Structure):
    _pack_ = 1

    _fields_ = [
        ("position", c_uint8),
        ("numLaps", c_uint8),
        ("gridPosition", c_uint8),
        ("points", c_uint8),
        ("numPitStops", c_uint8),
        ("resultStatus", c_uint8),
        ("bestLapTimeInMS", c_uint32),
        ("totalRaceTime", c_double),
        ("penaltiesTime", c_uint8),
        ("numPenalties", c_uint8),
        ("numTyreStints", c_uint8),
        ("tyreStintsActual", c_uint8 * 8),
        ("tyreStintsVisual", c_uint8 * 8),
        ("tyreStintsEndLaps", c_uint8 * 8),
    ]

    def to_dict(self):
        return {
            "position": self.position,
            "numLaps": self.numLaps,
            "gridPosition": self.gridPosition,
            "points": self.points,
            "numPitStops": self.numPitStops,
            "resultStatus": self.resultStatus,
            "bestLapTimeInMS": self.bestLapTimeInMS,
            "totalRaceTime": self.totalRaceTime,
            "penaltiesTime": self.penaltiesTime,
            "numPenalties": self.numPenalties,
            "numTyreStints": self.numTyreStints,
            "tyreStintsActual": list(self.tyreStintsActual),
            "tyreStintsVisual": list(self.tyreStintsVisual),
            "tyreStintsEndLaps": list(self.tyreStintsEndLaps),
        }


class PacketFinalClassification(Structure):
    ARRAY_NAME = "classification_data"

    _pack_ = 1

    _fields_ = [
        ("header", PacketHeader),
        ("numCars", c_uint8),
        (
            "classificationData",
            FinalClassificationData * Packet.MAX_NUMBER_OF_PARTICIPANTS,
        ),
    ]

    def to_dict(self):
        classification_dicts = [
            self.classificationData[i].to_dict()
            for i in range(Packet.MAX_NUMBER_OF_PARTICIPANTS)
        ]
        return {
            "header": self.header.to_dict(),
            "numCars": self.numCars,
            self.ARRAY_NAME: classification_dicts,
        }
