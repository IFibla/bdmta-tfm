from ctypes import Structure, c_float, c_uint8
from .packetHeader import PacketHeader

MAX_MARSHALL_ZONES = 21
MAX_NUMBER_OF_PARTICIPANTS = 22
MAX_WEATHER_FORECAST_SAMPLES = 56


class CarSetupData(Structure):
    _pack_ = 1

    _fields_ = [
        ("front_wing", c_uint8),
        ("rear_wing", c_uint8),
        ("on_throttle", c_uint8),
        ("off_throttle", c_uint8),
        ("front_camber", c_float),
        ("rear_camber", c_float),
        ("front_toe", c_float),
        ("rear_toe", c_float),
        ("front_suspension", c_uint8),
        ("rear_suspension", c_uint8),
        ("front_anti_roll_bar", c_uint8),
        ("rear_anti_roll_bar", c_uint8),
        ("front_suspension_height", c_uint8),
        ("rear_suspension_height", c_uint8),
        ("break_pressure", c_uint8),
        ("break_bias", c_uint8),
        ("rear_left_tyre_pressure", c_float),
        ("rear_right_tyre_pressure", c_float),
        ("front_left_tyre_pressure", c_float),
        ("front_right_tyre_pressure", c_float),
        ("ballast", c_uint8),
        ("fuel_load", c_float),
    ]

    def to_dict(self):
        return {field[0]: float(getattr(self, field[0])) for field in self._fields_}


class PacketSetups(Structure):
    ARRAY_NAME = "car_setup"

    _pack_ = 1

    _fields_ = [
        ("header", PacketHeader),
        ("car_setup", CarSetupData * MAX_NUMBER_OF_PARTICIPANTS),
    ]

    def to_dict(self):
        return {
            "header": self.header.to_dict(),
            self.ARRAY_NAME: [
                self.car_setup[i].to_dict() for i in range(MAX_NUMBER_OF_PARTICIPANTS)
            ],
        }
