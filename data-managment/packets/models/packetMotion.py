from ctypes import Structure, c_float, c_int16
from .packetHeader import PacketHeader
from ..packets import Packet


class CarMotion(Structure):
    _pack_ = 1

    _fields_ = [
        ("world_position_x", c_float),
        ("world_position_y", c_float),
        ("world_position_z", c_float),
        ("world_velocity_x", c_float),
        ("world_velocity_y", c_float),
        ("world_velocity_z", c_float),
        ("world_forward_direction_x", c_int16),
        ("world_forward_direction_y", c_int16),
        ("world_forward_direction_z", c_int16),
        ("world_right_direction_x", c_int16),
        ("world_right_direction_y", c_int16),
        ("world_right_direction_z", c_int16),
        ("g_force_lateral", c_float),
        ("g_force_longitudinal", c_float),
        ("g_force_vertical", c_float),
        ("yaw", c_float),
        ("pitch", c_float),
        ("roll", c_float),
    ]

    def to_dict(self):
        return {field[0]: getattr(self, field[0]) for field in self._fields_}


class PacketMotion(Structure):
    ARRAY_NAME = "car_motion"

    _pack_ = 1

    _fields_ = [
        ("header", PacketHeader),
        ("car_motion", CarMotion * Packet.MAX_NUMBER_OF_PARTICIPANTS),
        ("suspension_position", c_float * 4),
        ("suspension_velocity", c_float * 4),
        ("suspension_acceleration", c_float * 4),
        ("wheel_speed", c_float * 4),
        ("wheel_slip", c_float * 4),
        ("local_velocity_x", c_float),
        ("local_velocity_y", c_float),
        ("local_velocity_z", c_float),
        ("angular_velocity_x", c_float),
        ("angular_velocity_y", c_float),
        ("angular_velocity_z", c_float),
        ("angular_acceleration_x", c_float),
        ("angular_acceleration_y", c_float),
        ("angular_acceleration_z", c_float),
        ("front_wheels_angle", c_float),
    ]

    def to_dict(self):
        motion_dicts = [
            self.car_motion[i].to_dict()
            for i in range(Packet.MAX_NUMBER_OF_PARTICIPANTS)
        ]
        return {
            "header": self.header.to_dict(),
            self.ARRAY_NAME: motion_dicts,
            "suspension_position": [self.suspension_position[i] for i in range(4)],
            "suspension_velocity": [self.suspension_velocity[i] for i in range(4)],
            "suspension_acceleration": [
                self.suspension_acceleration[i] for i in range(4)
            ],
            "wheel_speed": [self.wheel_speed[i] for i in range(4)],
            "wheel_slip": [self.wheel_slip[i] for i in range(4)],
            "local_velocity_x": self.local_velocity_x,
            "local_velocity_y": self.local_velocity_y,
            "local_velocity_z": self.local_velocity_z,
            "angular_velocity_x": self.angular_velocity_x,
            "angular_velocity_y": self.angular_velocity_y,
            "angular_velocity_z": self.angular_velocity_z,
            "angular_acceleration_x": self.angular_acceleration_x,
            "angular_acceleration_y": self.angular_acceleration_y,
            "angular_acceleration_z": self.angular_acceleration_z,
            "front_wheels_angle": self.front_wheels_angle,
        }
