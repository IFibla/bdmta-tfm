from ctypes import Structure, c_float, c_uint8, c_uint16, c_uint32, c_uint64


class PacketHeader(Structure):
    _pack_ = 1

    _fields_ = [
        ("packet_format", c_uint16),
        ("game_major_version", c_uint8),
        ("game_minor_version", c_uint8),
        ("packet_version", c_uint8),
        ("packet_id", c_uint8),
        ("session_uid", c_uint64),
        ("session_time", c_float),
        ("frame_identifier", c_uint32),
        ("player_car_index", c_uint8),
        ("secondary_player_car_index", c_uint8),
    ]

    def to_dict(self):
        return {field[0]: float(getattr(self, field[0])) for field in self._fields_}
