from datetime import datetime, timedelta
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon, Point
import json


def read_tle_file(file_path):
    with open(file_path, "r") as file:
        tle_lines = file.read().splitlines()
    return tle_lines


def plot_position(positions_and_velocities, colors=None):
    # Plot 3D graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    if colors is None:
        colors = np.arange(len(positions_and_velocities))

    scatter = ax.scatter(
        positions_and_velocities[:, 0],
        positions_and_velocities[:, 1],
        positions_and_velocities[:, 2],
        c=colors,
        cmap="viridis",  # You can change the colormap as needed
        s=1,
    )

    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.set_zlabel("Z (km)")
    ax.set_title("Satellite Positions")

    # Add colorbar to show satellite index or another relevant information
    cbar = plt.colorbar(scatter, label="Satellite Index")
    cbar.set_ticks(np.arange(len(positions_and_velocities)))

    plt.show()


def compute_satellite_position(tle_lines, start_time, end_time, time_interval):
    satellites = []

    for i in range(0, len(tle_lines), 2):
        line1 = tle_lines[i]
        line2 = tle_lines[i + 1]
        satellite = twoline2rv(line1, line2, wgs72)
        satellites.append(satellite)

    total_seconds = int((end_time - start_time).total_seconds())
    time_points = np.arange(0, total_seconds + 1, time_interval)

    positions_and_velocities = np.empty((len(time_points), 6), dtype=np.float64)

    current_time = np.datetime64(start_time) + np.timedelta64(0, "s")

    for i, time_point in enumerate(time_points):
        for j, satellite in enumerate(satellites):
            current_datetime = np.datetime64(current_time) + np.timedelta64(
                int(time_point), "s"
            )
            position, velocity = satellite.propagate(
                current_datetime.astype(datetime).year,
                current_datetime.astype(datetime).month,
                current_datetime.astype(datetime).day,
                current_datetime.astype(datetime).hour,
                current_datetime.astype(datetime).minute,
                current_datetime.astype(datetime).second,
            )
            positions_and_velocities[i, :3] = position
            positions_and_velocities[i, 3:] = velocity

    return positions_and_velocities


def is_within_area(positions, corner_points):
    # Check if each position is within the specified area

    # Create a Convex Hull from the corner points
    hull = ConvexHull(corner_points)

    # Get the vertices of the convex hull
    hull_vertices = hull.points[hull.vertices]

    # Create a Shapely Polygon from the convex hull vertices
    convex_polygon = Polygon(hull_vertices)

    # Check if each position is within the convex hull
    points = [Point(p) for p in positions[:, :2]]
    in_area = [convex_polygon.contains(point) for point in points]

    return np.array(in_area)


# Example usage:
tle_file_path = "./30sats.txt"
start_time = datetime(2024, 1, 1, 0, 0, 0)
end_time = start_time + timedelta(days=1)
time_interval = 1  # seconds

tle_lines = read_tle_file(tle_file_path)
positions_and_velocities = compute_satellite_position(
    tle_lines, start_time, end_time, time_interval
)

# Plot the positions around the earth.
plot_position(positions_and_velocities)

# Specify the corner points of the rectangle
rectangle_corner_points = np.array(
    [
        [1719.9673, -2444.58196],
        [1727.74973, -2442.64459],
        [1729.09096, -2450.71009],
        [-31.32309, -147.79778],
    ]
)

# Convert to a list of dictionaries
data_list = []
for i in range(len(positions_and_velocities)):
    data_list.append(
        {
            "time": str(start_time + timedelta(seconds=i)),
            "position": positions_and_velocities[i, :3].tolist(),
            "velocity": positions_and_velocities[i, 3:].tolist(),
        }
    )

# Dump data to a JSON file
with open("satellite_data.json", "w", encoding="utf-8") as json_file:
    json.dump(data_list, json_file, indent=2)


# Check if the satellite is within the specified rectangle
in_area_mask = is_within_area(positions_and_velocities[:, :2], rectangle_corner_points)

print(in_area_mask)
# Print or use the information as needed
print(
    f"The satellite is within the specified rectangle at some point: {np.any(in_area_mask)}"
)
