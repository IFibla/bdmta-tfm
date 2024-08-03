from ctypes import Structure, c_float, c_int8, c_uint8, c_uint16, c_uint32
from .packetHeader import PacketHeader
from ..packets import Packet


class MarshallZone(Structure):
    _pack_ = 1

    _fields_ = [("zone_start", c_float), ("zone_flag", c_int8)]

    def to_dict(self):
        return {field[0]: getattr(self, field[0]) for field in self._fields_}


class WeatherForecastSample(Structure):
    _pack_ = 1

    _fields_ = [
        ("session_type", c_uint8),
        ("time_offset", c_uint8),
        ("weather", c_uint8),
        ("track_temperature", c_int8),
        ("track_temperature_change", c_int8),
        ("air_temperature", c_int8),
        ("air_temperature_change", c_int8),
        ("rain_percentage", c_uint8),
    ]

    def to_dict(self):
        return {field[0]: getattr(self, field[0]) for field in self._fields_}


class PacketSession(Structure):
    _pack_ = 1

    _fields_ = [
        ("header", PacketHeader),
        ("weather", c_uint8),
        ("track_temperature", c_int8),
        ("air_temperature", c_int8),
        ("total_laps", c_uint8),
        ("session_type", c_uint8),
        ("track_id", c_int8),
        ("formula", c_uint8),
        ("session_time_left", c_uint16),
        ("session_duration", c_uint16),
        ("pit_speed_limit", c_uint8),
        ("game_paused", c_uint8),
        ("is_spectating", c_uint8),
        ("spectator_car_index", c_uint8),
        ("sli_pro_native_support", c_uint8),
        ("number_marshall_zones", c_uint8),
        ("marshall_zones", MarshallZone * Packet.MAX_MARSHALL_ZONES),
        ("safety_car_status", c_uint8),
        ("network_game", c_uint8),
        ("number_forecast_samples", c_uint8),
        (
            "weather_forecast_samples",
            WeatherForecastSample * Packet.MAX_WEATHER_FORECAST_SAMPLES,
        ),
        ("forecast_accuracy", c_uint8),
        ("ai_difficulty", c_uint8),
        ("season_link_identifier", c_uint32),
        ("weekend_link_identifier", c_uint32),
        ("session_link_identifier", c_uint32),
        ("pit_stop_window_ideal_lap", c_uint8),
        ("pit_stop_window_last_lap", c_uint8),
        ("pit_stop_rejoin_position", c_uint8),
        ("steering_assist", c_uint8),
        ("breaking_assist", c_uint8),
        ("gearbox_assist", c_uint8),
        ("pit_assist", c_uint8),
        ("pit_release_assist", c_uint8),
        ("ers_assist", c_uint8),
        ("drs_assist", c_uint8),
        ("dynamic_racing_line", c_uint8),
        ("dynamic_racing_line_type", c_uint8),
        ("game_mode", c_uint8),
        ("rule_set", c_uint8),
        ("time_of_day", c_uint32),
        ("session_length", c_uint8),
    ]

    def to_dict(self):
        return {
            "header": self.header.to_dict(),
            "weather": self.weather,
            "track_temperature": self.track_temperature,
            "air_temperature": self.air_temperature,
            "total_laps": self.total_laps,
            "session_type": self.session_type,
            "track_id": self.track_id,
            "formula": self.formula,
            "session_time_left": self.session_time_left,
            "session_duration": self.session_duration,
            "pit_speed_limit": self.pit_speed_limit,
            "game_paused": self.game_paused,
            "is_spectating": self.is_spectating,
            "spectator_car_index": self.spectator_car_index,
            "sli_pro_native_support": self.sli_pro_native_support,
            "number_marshall_zones": self.number_marshall_zones,
            "marshall_zones": [
                self.marshall_zones[i].to_dict()
                for i in range(Packet.MAX_MARSHALL_ZONES)
            ],
            "safety_car_status": self.safety_car_status,
            "network_game": self.network_game,
            "number_forecast_samples": self.number_forecast_samples,
            "weather_forecast_samples": [
                self.weather_forecast_samples[i].to_dict()
                for i in range(Packet.MAX_WEATHER_FORECAST_SAMPLES)
            ],
            "forecast_accuracy": self.forecast_accuracy,
            "ai_difficulty": self.ai_difficulty,
            "season_link_identifier": self.season_link_identifier,
            "weekend_link_identifier": self.weekend_link_identifier,
            "session_link_identifier": self.session_link_identifier,
            "pit_stop_window_ideal_lap": self.pit_stop_window_ideal_lap,
            "pit_stop_window_last_lap": self.pit_stop_window_last_lap,
            "pit_stop_rejoin_position": self.pit_stop_rejoin_position,
            "steering_assist": self.steering_assist,
            "breaking_assist": self.breaking_assist,
            "gearbox_assist": self.gearbox_assist,
            "pit_assist": self.pit_assist,
            "pit_release_assist": self.pit_release_assist,
            "ers_assist": self.ers_assist,
            "drs_assist": self.drs_assist,
            "dynamic_racing_line": self.dynamic_racing_line,
            "dynamic_racing_line_type": self.dynamic_racing_line_type,
            "game_mode": self.game_mode,
            "rule_set": self.rule_set,
            "time_of_day": self.time_of_day,
            "session_length": self.session_length,
        }
