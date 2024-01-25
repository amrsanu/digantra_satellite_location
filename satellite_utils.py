"""satellite_utils.py"""

from datetime import datetime
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
import numpy as np
import pyproj
from shapely.geometry import Polygon, Point


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
    with open(file_path, "r", encoding="utf-8") as file:
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


def vectorized_ecef2lla(positions_array):
    """Takes numpy array [satellite : time : Pxyz] as input in list format and
    returns positions_array_lla (longitude, latitude, and altitude)"""

    ecef = pyproj.Proj(proj="geocent", ellps="WGS84", datum="WGS84")
    lla = pyproj.Proj(proj="latlong", ellps="WGS84", datum="WGS84")

    # Reshape the positions_array to a 2D array for vectorization
    flattened_positions = positions_array.reshape(-1, 3)
    print(f"Shape - flattened_positions: {flattened_positions.shape}")

    # Vectorize the transformation functions
    vec_ecef2lla = np.vectorize(pyproj.transform)

    # Apply the vectorized function to each point
    lona, lata, alta = vec_ecef2lla(
        ecef,
        lla,
        flattened_positions[:, 0],
        flattened_positions[:, 1],
        flattened_positions[:, 2],
        radians=False,
    )

    # Reshape the result back to the original shape
    positions_array_lla = np.column_stack((lona, lata, alta)).reshape(
        positions_array.shape
    )
    # return positions_array_lla

    return positions_array_lla


def filter_positions_within_region(positions, corner_points):
    """
    Filter satellite positions based on the region defined by four corner points.

    Parameters:
    - positions (numpy.ndarray): Array containing longitude and latitude for each satellite.
      Shape: (num_satellites, num_time_points, 2)
    - corner_points (numpy.ndarray): Array containing the four corner points.
      Shape: (4, 2)

    Returns:
    - numpy.ndarray: Satellite positions that fall within the region.
      Shape: (num_satellites, num_time_points, 2)
    """
    num_satellites, num_time_points, _ = positions.shape

    # Reshape positions array for vectorized processing
    flattened_positions = positions.reshape(-1, 2)
    # print(f"Positions: {flattened_positions}")

    # Create a Shapely Polygon from the corner points
    polygon = Polygon(corner_points[:, :2])

    # Create Shapely Point objects for each position
    points = [Point(p) for p in flattened_positions]

    # Check if each point is within the polygon
    in_region_mask = np.array([polygon.contains(point) for point in points])
    # Reshape the result back to the original shape
    in_region_mask = in_region_mask.reshape(num_satellites, num_time_points)

    # Filter positions based on the region mask
    filtered_positions = positions[in_region_mask]

    return filtered_positions
