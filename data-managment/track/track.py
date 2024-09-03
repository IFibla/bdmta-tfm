from .layouts.redbull_ring import waypoints


class Track:
    """
    A class to represent a race track and perform various operations related to waypoints and positions.

    This class provides static methods to:
    - Find the closest value in waypoints based on 3D coordinates.
    - Get the category of a specific point.
    - Compare positions within a given DataFrame.
    """

    @staticmethod
    def find_closest_value(_x, _y, _z):
        """
        Finds the closest waypoint to the given coordinates (_x, _y, _z) and returns the associated value.

        Parameters:
        ----------
        _x : float
            The x-coordinate of the point to compare.
        _y : float
            The y-coordinate of the point to compare.
        _z : float
            The z-coordinate of the point to compare.

        Returns:
        -------
        float
            The associated value (4th element) of the closest waypoint.
        """
        distances = [
            (((_x - x) ** 2) + ((_y - y) ** 2) + ((_z - z) ** 2)) ** 0.5
            for x, y, z, _, _ in waypoints
        ]
        min_index = distances.index(min(distances))
        return waypoints[min_index][3]

    @staticmethod
    def get_point_category(point):
        """
        Returns the category of the specified point from the waypoints list.

        Parameters:
        ----------
        point : any
            The point to find the category for.

        Returns:
        -------
        any
            The category (5th element) of the specified point if found, otherwise None.
        """
        for _, _, _, p, c in waypoints:
            if point == c:
                return c
        return None

    @staticmethod
    def compare_positions(df):
        """
        Compares positions within the given DataFrame to identify instances of significant positional improvement.

        The method:
        - Removes duplicate rows.
        - Sorts the DataFrame by session time.
        - Calculates previous positions by shifting the position column.
        - Filters the DataFrame to include only cases where the current position is significantly better than the previous one.

        Parameters:
        ----------
        df : pandas.DataFrame
            A DataFrame containing columns such as session time, position, and other race-related data.

        Returns:
        -------
        pandas.DataFrame
            A DataFrame filtered to include session type, driver, and session time
            where there are significant positional improvements.
        """
        df.drop_duplicates(inplace=True)
        df.sort_values(by=["session_time"], inplace=True)
        df["prev_position"] = df["position"].shift(1)
        df = df[
            (df["position"] < df["prev_position"])
            & (df["position"] < 0.05)
            & (0.95 < df["prev_position"])
        ][["session_type", "driver", "session_time"]]
        df.drop_duplicates(inplace=True)
        return df
