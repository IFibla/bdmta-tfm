from .layouts.redbull_ring import waypoints


class Track:
    @staticmethod
    def find_closest_value(_x, _y, _z):
        distances = [
            (((_x - x) ** 2) + ((_y - y) ** 2) + ((_z - z) ** 2)) ** 0.5
            for x, y, z, _ in waypoints
        ]
        min_index = distances.index(min(distances))
        return waypoints[min_index][3]

    @staticmethod
    def split_by_laps(driver_packets):
        laps = []
        current_lap = []
        last_position = None
        for packet in driver_packets:
            if "world_position_perc" in packet:
                if (
                    last_position is None
                    or last_position < packet["world_position_perc"]
                ):
                    current_lap.append(packet)
                else:
                    laps.append(current_lap)
                    current_lap = []
                last_position = packet["world_position_perc"]
            else:
                current_lap.append(packet)
        laps.append(current_lap)
        return laps

    @staticmethod
    def add_lap_number(driver_packets):
        packet_laps = []
        current_lap = 1
        last_position = None

        for packet in driver_packets:
            if "world_position_perc" in packet:
                if (
                    last_position is not None
                    and packet["world_position_perc"] < last_position
                ):
                    current_lap += 1
                last_position = packet["world_position_perc"]
            packet_laps.append(current_lap)

        return packet_laps
