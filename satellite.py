# main_script.py

from datetime import datetime, timedelta
from satellite_utils import Satellite, read_tle_file, compute_satellite_position
from visualization_utils import visualize_satellite_positions


def main():
    tle_file_path = "./30sats.txt"
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    end_time = start_time + timedelta(days=1)
    time_interval = 1  # seconds

    tle_lines = read_tle_file(tle_file_path)
    satellites = [
        Satellite(tle_lines[i], tle_lines[i + 1]) for i in range(0, len(tle_lines), 2)
    ]

    # Get satellite data
    positions_array = compute_satellite_position(
        satellites, start_time, end_time, time_interval
    )

    # Visualize satellite positions with different colors
    visualize_satellite_positions(positions_array, save_path="satellite_positions.png")


if __name__ == "__main__":
    main()
