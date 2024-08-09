from ctypes import Structure, c_float, c_uint8
from .packetHeader import PacketHeader

MAX_MARSHALL_ZONES = 21
MAX_NUMBER_OF_PARTICIPANTS = 22
MAX_WEATHER_FORECAST_SAMPLES = 56


class CarDamageData(Structure):
    _pack_ = 1

    _fields_ = [
        ("rear_left_tyresWear", c_float),
        ("rear_right_tyresWear", c_float),
        ("front_left_tyresWear", c_float),
        ("front_right_tyresWear", c_float),
        ("rear_left_tyresDamage", c_uint8),
        ("rear_right_tyresDamage", c_uint8),
        ("front_left_tyresDamage", c_uint8),
        ("front_right_tyresDamage", c_uint8),
        ("rear_left_brakesDamage", c_uint8),
        ("rear_right_brakesDamage", c_uint8),
        ("front_left_brakesDamage", c_uint8),
        ("front_right_brakesDamage", c_uint8),
        ("frontLeftWingDamage", c_uint8),
        ("frontRightWingDamage", c_uint8),
        ("rearWingDamage", c_uint8),
        ("floorDamage", c_uint8),
        ("diffuserDamage", c_uint8),
        ("sidepodDamage", c_uint8),
        ("drsFault", c_uint8),
        ("ersFault", c_uint8),
        ("gearBoxDamage", c_uint8),
        ("engineDamage", c_uint8),
        ("engineMGUHWear", c_uint8),
        ("engineESWear", c_uint8),
        ("engineCEWear", c_uint8),
        ("engineICEWear", c_uint8),
        ("engineMGUKWear", c_uint8),
        ("engineTCWear", c_uint8),
        ("engineBlown", c_uint8),
        ("engineSeized", c_uint8),
    ]

    def to_dict(self):
        return {field[0]: float(getattr(self, field[0])) for field in self._fields_}


class PacketCarDamage(Structure):
    ARRAY_NAME = "car_damage_data"

    _pack_ = 1

    _fields_ = [
        ("header", PacketHeader),
        ("carDamageData", CarDamageData * MAX_NUMBER_OF_PARTICIPANTS),
    ]

    def to_dict(self):
        return {
            "header": self.header.to_dict(),
            self.ARRAY_NAME: [
                self.carDamageData[i].to_dict()
                for i in range(MAX_NUMBER_OF_PARTICIPANTS)
            ],
        }
