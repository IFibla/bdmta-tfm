from ctypes import Structure, c_float, c_uint8
from .packetHeader import PacketHeader
from ..packets import Packet


class CarDamageData(Structure):
    _pack_ = 1

    _fields_ = [
        ("tyresWear", c_float * 4),
        ("tyresDamage", c_uint8 * 4),
        ("brakesDamage", c_uint8 * 4),
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
        return {
            "tyresWear": list(self.tyresWear),
            "tyresDamage": list(self.tyresDamage),
            "brakesDamage": list(self.brakesDamage),
            "frontLeftWingDamage": self.frontLeftWingDamage,
            "frontRightWingDamage": self.frontRightWingDamage,
            "rearWingDamage": self.rearWingDamage,
            "floorDamage": self.floorDamage,
            "diffuserDamage": self.diffuserDamage,
            "sidepodDamage": self.sidepodDamage,
            "drsFault": self.drsFault,
            "ersFault": self.ersFault,
            "gearBoxDamage": self.gearBoxDamage,
            "engineDamage": self.engineDamage,
            "engineMGUHWear": self.engineMGUHWear,
            "engineESWear": self.engineESWear,
            "engineCEWear": self.engineCEWear,
            "engineICEWear": self.engineICEWear,
            "engineMGUKWear": self.engineMGUKWear,
            "engineTCWear": self.engineTCWear,
            "engineBlown": self.engineBlown,
            "engineSeized": self.engineSeized,
        }


class PacketCarDamage(Structure):
    ARRAY_NAME = "car_damage_data"

    _pack_ = 1

    _fields_ = [
        ("header", PacketHeader),
        ("carDamageData", CarDamageData * Packet.MAX_NUMBER_OF_PARTICIPANTS),
    ]

    def to_dict(self):
        car_damage_dicts = [
            self.carDamageData[i].to_dict()
            for i in range(Packet.MAX_NUMBER_OF_PARTICIPANTS)
        ]
        return {
            "header": self.header.to_dict(),
            self.ARRAY_NAME: car_damage_dicts,
        }
