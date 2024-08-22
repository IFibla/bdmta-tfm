from .layouts.redbull_ring import waypoints
import pandas as pd


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
    def _rewrite_df(generator, lap):
        rows = pd.concat(generator, ignore_index=True)
        rows.sort_values(by=["session_time"], inplace=True)

        if not any(rows["lap"] != -1):
            rows.iloc[0, rows.columns.get_loc("lap")] = lap

        for i in range(1, len(rows)):
            if rows.iloc[i].position == -1:
                rows.iloc[i, rows.columns.get_loc("lap")] = lap
                rows.iloc[i, rows.columns.get_loc("position")] = rows.iloc[
                    i - 1
                ].position
            elif rows.iloc[i - 1].position > rows.iloc[i].position:
                lap += 1
                rows.iloc[i, rows.columns.get_loc("lap")] = lap
            else:
                rows.iloc[i, rows.columns.get_loc("lap")] = lap

        return rows, lap

    @staticmethod
    def add_laps(key, pdf_iter, state):
        current_lap = state.get[0] if state.exists else 1
        pdf_iter, lap = Track._rewrite_df(pdf_iter, current_lap)
        state.update((lap,))
        yield pdf_iter
