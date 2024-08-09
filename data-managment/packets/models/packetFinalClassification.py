from ctypes import Structure, c_uint8, c_uint32, c_double
from .packetHeader import PacketHeader

MAX_MARSHALL_ZONES = 21
MAX_NUMBER_OF_PARTICIPANTS = 22
MAX_WEATHER_FORECAST_SAMPLES = 56


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
        ("tyreStintsActual_0", c_uint8),
        ("tyreStintsActual_1", c_uint8),
        ("tyreStintsActual_2", c_uint8),
        ("tyreStintsActual_3", c_uint8),
        ("tyreStintsActual_4", c_uint8),
        ("tyreStintsActual_5", c_uint8),
        ("tyreStintsActual_6", c_uint8),
        ("tyreStintsActual_7", c_uint8),
        ("tyreStintsVisual_0", c_uint8),
        ("tyreStintsVisual_1", c_uint8),
        ("tyreStintsVisual_2", c_uint8),
        ("tyreStintsVisual_3", c_uint8),
        ("tyreStintsVisual_4", c_uint8),
        ("tyreStintsVisual_5", c_uint8),
        ("tyreStintsVisual_6", c_uint8),
        ("tyreStintsVisual_7", c_uint8),
        ("tyreStintsEndLaps_0", c_uint8),
        ("tyreStintsEndLaps_1", c_uint8),
        ("tyreStintsEndLaps_2", c_uint8),
        ("tyreStintsEndLaps_3", c_uint8),
        ("tyreStintsEndLaps_4", c_uint8),
        ("tyreStintsEndLaps_5", c_uint8),
        ("tyreStintsEndLaps_6", c_uint8),
        ("tyreStintsEndLaps_7", c_uint8),
    ]

    def to_dict(self):
        return {field[0]: float(getattr(self, field[0])) for field in self._fields_}


class PacketFinalClassification(Structure):
    ARRAY_NAME = "classification_data"

    _pack_ = 1

    _fields_ = [
        ("header", PacketHeader),
        ("numCars", c_uint8),
        (
            "classificationData",
            FinalClassificationData * MAX_NUMBER_OF_PARTICIPANTS,
        ),
    ]

    def to_dict(self):
        return {
            "header": self.header.to_dict(),
            self.ARRAY_NAME: [
                self.classificationData[i].to_dict()
                for i in range(MAX_NUMBER_OF_PARTICIPANTS)
            ],
            "numCars": self.numCars,
        }
