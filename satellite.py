# main_script.py
"""
Main script for computing satellite positions and filtering based on a specified region.

This script reads Two-Line Element (TLE) data, computes satellite positions, applies a filter based on a defined region,
and saves the results to files. It utilizes multi-threading for parallel computation of satellite positions.

Author: [Your Name]
Date: [Current Date]
"""

import json
import time
from datetime import datetime, timedelta
import numpy as np
from satellite_utils import (
    Satellite,
    read_tle_file,
    compute_satellite_position,
    vectorized_ecef2lla,
    filter_positions_within_region,
)
from concurrent.futures import ThreadPoolExecutor

# from visualization_utils import visualize_satellite_positions

# Constants
DAYS = 5
TLE_FILE_PATH = "./30sats.txt"
TIME_INTERVAL = 1  # seconds
START_TIME = datetime(2024, 1, 20, 0, 0, 0)

# Corner points of the region in the format [latitude, longitude, altitude]
CORNER_POINTS = np.array(
    [
        [25.44859843, -100.0, 70],
        [25.448, -70.0, 70],
        [25.46997504, -70.5, 70],
        [25.46997504, -100.5, 70],
    ]
)


def numpy_array_to_json(numpy_array, json_file_path):
    """
    Dump a NumPy array to a JSON file.

    Parameters:
    - numpy_array (numpy.ndarray): The NumPy array to be dumped.
    - json_file_path (str): The path to the JSON file.

    Returns:
    - None
    """
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(numpy_array.tolist(), json_file)


def satellite_position(time, satellites, start_time, end_time, time_interval):
    """
    Compute satellite positions for a specific time period and save the results.

    Parameters:
    - time (str): String representation of the time.
    - satellites (list): List of Satellite objects.
    - start_time (datetime): Start time for computation.
    - end_time (datetime): End time for computation.
    - time_interval (int): Time interval in seconds between position calculations.

    Returns:
    - None
    """
    time = time.split(" ")[0]
    print(f"Computing {time} satellite position.")
    # Get satellite data
    positions_array = compute_satellite_position(
        satellites, start_time, end_time, time_interval
    )
    print(f"Shape - positions_array: {positions_array.shape}")

    # Apply the vectorized function to positions_array
    positions_array_lla = vectorized_ecef2lla(positions_array)
    np.save(f"positions_array_lla_{time}.npy", positions_array_lla)
    positions_array_ll = positions_array_lla[:, :, :2]
    np.save(f"positions_array_ll_{time}.npy", positions_array_ll)


def filter_positions(start_time):
    """
    Filter satellite positions based on a specified region and save the filtered results.

    Parameters:
    - start_time (str): String representation of the start time.

    Returns:
    - numpy.ndarray: Filtered satellite positions.
    """
    start_time = start_time.split(" ")[0]
    positions_array_ll = np.load(f"positions_array_ll_{start_time}.npy")
    positions_array_lla = np.load(f"positions_array_lla_{start_time}.npy")

    # Example Usage:
    # positions_array_lla is assumed to have shape (num_satellites, num_time_points, 2)
    # corner_points is a 4x2 array representing the corner points of the region

    # Filter positions based on the region defined by corner points
    filtered_positions = filter_positions_within_region(
        positions_array_ll, CORNER_POINTS
    )

    # Print or use the filtered positions as needed
    print(f"Filtered Satellite Positions within the Region {start_time}:")
    return filtered_positions


def process_day(day, tle_lines):
    """
    Process satellite positions for a specific day.

    Parameters:
    - day (int): Day index.
    - tle_lines (list): List of Two-Line Element (TLE) data.

    Returns:
    - None
    """
    satellites = [
        Satellite(tle_lines[i], tle_lines[i + 1]) for i in range(0, len(tle_lines), 2)
    ]

    start_time = START_TIME + timedelta(days=day)
    end_time = start_time + timedelta(days=1)
    satellite_position(str(start_time), satellites, start_time, end_time, TIME_INTERVAL)
    filtered_positions = filter_positions(str(start_time))
    print(f"{day} : {filtered_positions}")


def main():
    """
    Main function for executing the script.

    Returns:
    - None
    """
    tle_lines = read_tle_file(TLE_FILE_PATH)

    with ThreadPoolExecutor() as executor:
        # Use executor.map to process each day in parallel
        executor.map(lambda day: process_day(day, tle_lines), range(DAYS))


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    execution_time = end - start
    print(f"Total execution time: {execution_time:.2f} seconds")
