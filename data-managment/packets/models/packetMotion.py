from ctypes import Structure, c_float, c_int16
from .packetHeader import PacketHeader

MAX_MARSHALL_ZONES = 21
MAX_NUMBER_OF_PARTICIPANTS = 22
MAX_WEATHER_FORECAST_SAMPLES = 56


class CarMotionData(Structure):
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
        return {field[0]: float(getattr(self, field[0])) for field in self._fields_}

    @classmethod
    def speed_layer_filter(cls, packet: dict[str, float]) -> dict[str, float]:
        return {
            field: packet[field]
            for field in [
                "world_position_x",
                "world_position_y",
                "world_position_z",
            ]
        }


class PacketMotion(Structure):
    ARRAY_NAME = "car_motion"

    _pack_ = 1

    _fields_ = [
        ("header", PacketHeader),
        ("car_motion", CarMotionData * MAX_NUMBER_OF_PARTICIPANTS),
        ("rear_left_suspension_position", c_float),
        ("rear_right_suspension_position", c_float),
        ("front_left_suspension_position", c_float),
        ("front_right_suspension_position", c_float),
        ("rear_left_suspension_velocity", c_float),
        ("rear_right_suspension_velocity", c_float),
        ("front_left_suspension_velocity", c_float),
        ("front_right_suspension_velocity", c_float),
        ("rear_left_suspension_acceleration", c_float),
        ("rear_right_suspension_acceleration", c_float),
        ("front_left_suspension_acceleration", c_float),
        ("front_right_suspension_acceleration", c_float),
        ("rear_left_wheel_speed", c_float),
        ("rear_right_wheel_speed", c_float),
        ("front_left_wheel_speed", c_float),
        ("front_right_wheel_speed", c_float),
        ("rear_left_wheel_slip", c_float),
        ("rear_right_wheel_slip", c_float),
        ("front_left_wheel_slip", c_float),
        ("front_right_wheel_slip", c_float),
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
        return {
            "header": self.header.to_dict(),
            self.ARRAY_NAME: [
                self.car_motion[i].to_dict() for i in range(MAX_NUMBER_OF_PARTICIPANTS)
            ],
            "rear_left_suspension_position": float(self.rear_left_suspension_position),
            "rear_right_suspension_position": float(
                self.rear_right_suspension_position
            ),
            "front_left_suspension_position": float(
                self.front_left_suspension_position
            ),
            "front_right_suspension_position": float(
                self.front_right_suspension_position
            ),
            "rear_left_suspension_velocity": float(self.rear_left_suspension_velocity),
            "rear_right_suspension_velocity": float(
                self.rear_right_suspension_velocity
            ),
            "front_left_suspension_velocity": float(
                self.front_left_suspension_velocity
            ),
            "front_right_suspension_velocity": float(
                self.front_right_suspension_velocity
            ),
            "rear_left_suspension_acceleration": float(
                self.rear_left_suspension_acceleration
            ),
            "rear_right_suspension_acceleration": float(
                self.rear_right_suspension_acceleration
            ),
            "front_left_suspension_acceleration": float(
                self.front_left_suspension_acceleration
            ),
            "front_right_suspension_acceleration": float(
                self.front_right_suspension_acceleration
            ),
            "rear_left_wheel_speed": float(self.rear_left_wheel_speed),
            "rear_right_wheel_speed": float(self.rear_right_wheel_speed),
            "front_left_wheel_speed": float(self.front_left_wheel_speed),
            "front_right_wheel_speed": float(self.front_right_wheel_speed),
            "rear_left_wheel_slip": float(self.rear_left_wheel_slip),
            "rear_right_wheel_slip": float(self.rear_right_wheel_slip),
            "front_left_wheel_slip": float(self.front_left_wheel_slip),
            "front_right_wheel_slip": float(self.front_right_wheel_slip),
            "local_velocity_x": float(self.local_velocity_x),
            "local_velocity_y": float(self.local_velocity_y),
            "local_velocity_z": float(self.local_velocity_z),
            "angular_velocity_x": float(self.angular_velocity_x),
            "angular_velocity_y": float(self.angular_velocity_y),
            "angular_velocity_z": float(self.angular_velocity_z),
            "angular_acceleration_x": float(self.angular_acceleration_x),
            "angular_acceleration_y": float(self.angular_acceleration_y),
            "angular_acceleration_z": float(self.angular_acceleration_z),
            "front_wheels_angle": float(self.front_wheels_angle),
        }
