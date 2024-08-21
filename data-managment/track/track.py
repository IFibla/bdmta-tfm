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
