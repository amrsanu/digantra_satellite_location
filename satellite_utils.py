# satellite_utils.py

from datetime import datetime
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
import numpy as np


class Satellite:
    def __init__(self, line1, line2):
        """
        Initialize a Satellite object using TLE (Two-Line Element) data.

        Parameters:
        - line1 (str): First line of TLE data.
        - line2 (str): Second line of TLE data.
        """
        self.satellite = twoline2rv(line1, line2, wgs72)

    def propagate(self, current_datetime):
        """
        Propagate the satellite position at a given datetime.

        Parameters:
        - current_datetime (datetime): Datetime for which the position is calculated.

        Returns:
        - tuple: Position (X, Y, Z) of the satellite.
        """
        position, _ = self.satellite.propagate(
            current_datetime.year,
            current_datetime.month,
            current_datetime.day,
            current_datetime.hour,
            current_datetime.minute,
            current_datetime.second,
        )
        return position


def read_tle_file(file_path):
    """
    Read TLE data from a file.

    Parameters:
    - file_path (str): Path to the TLE file.

    Returns:
    - list: List of TLE lines.
    """
    with open(file_path, "r") as file:
        tle_lines = file.read().splitlines()
    return tle_lines


def compute_satellite_position(satellites, start_time, end_time, time_interval):
    """
    Compute satellite positions over time.

    Parameters:
    - satellites (list): List of Satellite objects.
    - start_time (datetime): Start time of the simulation.
    - end_time (datetime): End time of the simulation.
    - time_interval (int): Time interval between points in seconds.

    Returns:
    - numpy.ndarray: 3D array containing positions for each satellite at each time point.
    """
    total_seconds = int((end_time - start_time).total_seconds())
    time_points = np.arange(0, total_seconds + 1, time_interval)

    num_satellites = len(satellites)

    # Create a 3D array to store positions for each satellite at each time point
    positions_array = np.empty((num_satellites, len(time_points), 3), dtype=np.float64)

    current_time = np.datetime64(start_time) + np.timedelta64(0, "s")

    for j, satellite in enumerate(satellites):
        for i, time_point in enumerate(time_points):
            current_datetime = np.datetime64(current_time) + np.timedelta64(
                int(time_point), "s"
            )
            position = satellite.propagate(current_datetime.astype(datetime))
            positions_array[j, i, :] = position

    return positions_array
