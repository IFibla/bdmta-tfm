from ctypes import Structure, c_float, c_uint32, c_uint16, c_uint8
from .packetHeader import PacketHeader
from ..packets import Packet


class Lap(Structure):
    _pack_ = 1

    _fields_ = [
        ("last_lap_time_in_milliseconds", c_uint32),
        ("current_lap_time_in_milliseconds", c_uint32),
        ("sector_1_time_in_milliseconds", c_uint16),
        ("sector_2_time_in_milliseconds", c_uint16),
        ("lap_distance", c_float),
        ("total_distance", c_float),
        ("safety_car_delta", c_float),
        ("car_position", c_uint8),
        ("current_lap_number", c_uint8),
        ("pit_status", c_uint8),
        ("number_pit_stops", c_uint8),
        ("sector", c_uint8),
        ("current_lap_invalid", c_uint8),
        ("penalties", c_uint8),
        ("warnings", c_uint8),
        ("number_unserved_drive_through", c_uint8),
        ("number_unserved_stop_and_go", c_uint8),
        ("grid_position", c_uint8),
        ("driver_status", c_uint8),
        ("result_status", c_uint8),
        ("pit_lane_timer_active", c_uint8),
        ("pit_lane_time_in_lane_in_milliseconds", c_uint16),
        ("pit_stop_timer_in_milliseconds", c_uint16),
        ("pit_stop_should_serve_penalty", c_uint8),
    ]

    def to_dict(self):
        return {field[0]: getattr(self, field[0]) for field in self._fields_}


class PacketLap(Structure):
    ARRAY_NAME = "laps"

    _pack_ = 1

    _fields_ = [
        ("header", PacketHeader),
        ("lap", Lap * Packet.MAX_NUMBER_OF_PARTICIPANTS),
        ("time_trial_pb_car_index", c_uint8),
        ("time_trial_rival_car_index", c_uint8),
    ]

    def to_dict(self):
        lap_dicts = [
            self.lap[i].to_dict() for i in range(Packet.MAX_NUMBER_OF_PARTICIPANTS)
        ]
        return {
            "header": self.header.to_dict(),
            self.ARRAY_NAME: lap_dicts,
            "time_trial_pb_car_index": self.time_trial_pb_car_index,
            "time_trial_rival_car_index": self.time_trial_rival_car_index,
        }
