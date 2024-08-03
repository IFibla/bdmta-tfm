from ctypes import Structure, c_float, c_uint8, c_int8, c_uint16, c_uint32, c_uint64
from .packetHeader import PacketHeader
from ..packets import Packet


class CarTelemetry(Structure):
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
        ("brakes_temperature", c_uint16 * 4),
        ("tyres_surface_temperature", c_uint8 * 4),
        ("tyres_inner_temperature", c_uint8 * 4),
        ("engine_temperature", c_uint16 * 4),
        ("tyres_pressure", c_float * 4),
        ("surface_type", c_uint8 * 4),
    ]

    def to_dict(self):
        return {field[0]: getattr(self, field[0]) for field in self._fields_}


class PacketCarTelemetry(Structure):
    ARRAY_NAME = "car_telemetry"

    _pack_ = 1

    _fields_ = [
        ("header", PacketHeader),
        ("car_telemetry_data", CarTelemetry * Packet.MAX_NUMBER_OF_PARTICIPANTS),
        ("mfd_panel_index", c_uint8),
        ("mfd_panel_index_secondary_player", c_uint8),
        ("suggested_gear", c_int8),
    ]

    def to_dict(self):
        car_dicts = [
            self.car_telemetry_data[i].to_dict()
            for i in range(Packet.MAX_NUMBER_OF_PARTICIPANTS)
        ]
        return {
            "header": self.header.to_dict(),
            self.ARRAY_NAME: car_dicts,
            "mfd_panel_index": self.mfd_panel_index,
            "mfd_panel_index_secondary_player": self.mfd_panel_index_secondary_player,
            "suggested_gear": self.suggested_gear,
        }
