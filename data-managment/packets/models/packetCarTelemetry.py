from ctypes import Structure, c_float, c_uint8, c_int8, c_uint16, c_uint32, c_uint64
from .packetHeader import PacketHeader

MAX_MARSHALL_ZONES = 21
MAX_NUMBER_OF_PARTICIPANTS = 22
MAX_WEATHER_FORECAST_SAMPLES = 56


class CarTelemetryData(Structure):
    _pack_ = 1

    _fields_ = [
        ("speed", c_uint16),
        ("throttle", c_float),
        ("steer", c_float),
        ("brake", c_float),
        ("clutch", c_uint8),
        ("gear", c_int8),
        ("engine_rpm", c_uint16),
        ("drs", c_uint8),
        ("rev_lights_percent", c_uint8),
        ("rev_lights_bit_value", c_uint16),
        ("rear_left_brakes_temperature", c_uint16),
        ("rear_right_brakes_temperature", c_uint16),
        ("front_left_brakes_temperature", c_uint16),
        ("front_right_brakes_temperature", c_uint16),
        ("rear_left_tyres_surface_temperature", c_uint8),
        ("rear_right_tyres_surface_temperature", c_uint8),
        ("front_left_tyres_surface_temperature", c_uint8),
        ("front_right_tyres_surface_temperature", c_uint8),
        ("rear_left_tyres_inner_temperature", c_uint8),
        ("rear_right_tyres_inner_temperature", c_uint8),
        ("front_left_tyres_inner_temperature", c_uint8),
        ("front_right_tyres_inner_temperature", c_uint8),
        ("engine_temperature", c_uint16),
        ("rear_left_tyres_pressure", c_float),
        ("rear_right_tyres_pressure", c_float),
        ("front_left_tyres_pressure", c_float),
        ("front_right_tyres_pressure", c_float),
        ("rear_left_surface_type", c_uint8),
        ("rear_right_surface_type", c_uint8),
        ("front_left_surface_type", c_uint8),
        ("front_right_surface_type", c_uint8),
    ]

    def to_dict(self):
        return {field[0]: float(getattr(self, field[0])) for field in self._fields_}

    @classmethod
    def speed_layer_filter(cls, packet: dict[str, float]) -> dict[str, float]:
        return {
            field: packet[field]
            for field in [
                "speed",
                "throttle",
                "brake",
                "gear",
                "engine_rpm",
                "drs",
                "rear_left_brakes_temperature",
                "rear_right_brakes_temperature",
                "front_left_brakes_temperature",
                "front_right_brakes_temperature",
                "rear_left_tyres_surface_temperature",
                "rear_right_tyres_surface_temperature",
                "front_left_tyres_surface_temperature",
                "front_right_tyres_surface_temperature",
                "rear_left_tyres_inner_temperature",
                "rear_right_tyres_inner_temperature",
                "front_left_tyres_inner_temperature",
                "front_right_tyres_inner_temperature",
                "engine_temperature",
                "rear_left_tyres_pressure",
                "rear_right_tyres_pressure",
                "front_left_tyres_pressure",
                "front_right_tyres_pressure",
                "rear_left_surface_type",
                "rear_right_surface_type",
                "front_left_surface_type",
                "front_right_surface_type",
            ]
        }

    @classmethod
    def get_silver_layer_data(cls, packet: dict[str, float]) -> dict[str, float]:
        return {
            field: packet[field]
            for field in [
                "rear_left_brakes_temperature",
                "rear_right_brakes_temperature",
                "front_left_brakes_temperature",
                "front_right_brakes_temperature",
                "rear_left_tyres_surface_temperature",
                "rear_right_tyres_surface_temperature",
                "front_left_tyres_surface_temperature",
                "front_right_tyres_surface_temperature",
                "rear_left_tyres_inner_temperature",
                "rear_right_tyres_inner_temperature",
                "front_left_tyres_inner_temperature",
                "front_right_tyres_inner_temperature",
                "engine_temperature",
                "rear_left_tyres_pressure",
                "rear_right_tyres_pressure",
                "front_left_tyres_pressure",
                "front_right_tyres_pressure",
            ]
        }


class PacketCarTelemetry(Structure):
    ARRAY_NAME = "car_telemetry"

    _pack_ = 1

    _fields_ = [
        ("header", PacketHeader),
        ("car_telemetry_data", CarTelemetryData * MAX_NUMBER_OF_PARTICIPANTS),
        ("mfd_panel_index", c_uint8),
        ("mfd_panel_index_secondary_player", c_uint8),
        ("suggested_gear", c_int8),
    ]

    def to_dict(self):
        return {
            "header": self.header.to_dict(),
            self.ARRAY_NAME: [
                self.car_telemetry_data[i].to_dict()
                for i in range(MAX_NUMBER_OF_PARTICIPANTS)
            ],
            "mfd_panel_index": float(self.mfd_panel_index),
            "mfd_panel_index_secondary_player": float(
                self.mfd_panel_index_secondary_player
            ),
            "suggested_gear": float(self.suggested_gear),
        }
