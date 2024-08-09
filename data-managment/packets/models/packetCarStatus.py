from ctypes import Structure, c_float, c_uint8, c_uint16, c_int8
from .packetHeader import PacketHeader

MAX_MARSHALL_ZONES = 21
MAX_NUMBER_OF_PARTICIPANTS = 22
MAX_WEATHER_FORECAST_SAMPLES = 56


class CarStatusData(Structure):
    _pack_ = 1

    _fields_ = [
        ("tractionControl", c_uint8),
        ("antiLockBrakes", c_uint8),
        ("fuelMix", c_uint8),
        ("frontBrakeBias", c_uint8),
        ("pitLimiterStatus", c_uint8),
        ("fuelInTank", c_float),
        ("fuelCapacity", c_float),
        ("fuelRemainingLaps", c_float),
        ("maxRPM", c_uint16),
        ("idleRPM", c_uint16),
        ("maxGears", c_uint8),
        ("drsAllowed", c_uint8),
        ("drsActivationDistance", c_uint16),
        ("actualTyreCompound", c_uint8),
        ("visualTyreCompound", c_uint8),
        ("tyresAgeLaps", c_uint8),
        ("vehicleFiaFlags", c_int8),
        ("ersStoreEnergy", c_float),
        ("ersDeployMode", c_uint8),
        ("ersHarvestedThisLapMGUK", c_float),
        ("ersHarvestedThisLapMGUH", c_float),
        ("ersDeployedThisLap", c_float),
        ("networkPaused", c_uint8),
    ]

    def to_dict(self):
        return {field[0]: float(getattr(self, field[0])) for field in self._fields_}


class PacketCarStatus(Structure):
    ARRAY_NAME = "car_status_data"

    _pack_ = 1

    _fields_ = [
        ("header", PacketHeader),
        ("car_status", CarStatusData * MAX_NUMBER_OF_PARTICIPANTS),
    ]

    def to_dict(self):
        return {
            "header": self.header.to_dict(),
            self.ARRAY_NAME: [
                self.car_status[i].to_dict() for i in range(MAX_NUMBER_OF_PARTICIPANTS)
            ],
        }
