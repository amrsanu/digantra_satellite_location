# visualization_utils.py

import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon


def visualize_satellite_positions(positions_array, area_points=None, save_path=None):
    """
    Visualize satellite positions over time in a 3D space with different colors for each satellite.

    Parameters:
    - positions_array (numpy.ndarray): 3D array containing positions for each satellite at each time point.
      Shape: (num_satellites, num_time_points, 3)
    - area_points (numpy.ndarray): Optional. Array containing corner points of the area polygon in 3D.
      Shape: (num_vertices, 3)
    - save_path (str): Optional. If provided, the graph will be saved at the specified path.
    """
    num_satellites, num_time_points, _ = positions_array.shape

    # Create a list of unique colors for each satellite
    colors = plt.cm.viridis(np.linspace(0, 1, num_satellites))

    # Plot 3D graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    for i in range(area_points.shape[0]):
        x = area_points[i][0]
        y = area_points[i][1]
        z = area_points[i][2]

        ax.plot(x, y, z, color=colors[i], label=f"Satellite {i+1}")

    for i in range(num_satellites):
        x = positions_array[i, :, 0]
        y = positions_array[i, :, 1]
        z = positions_array[i, :, 2]

        ax.plot(x, y, z, color=colors[i], label=f"Satellite {i+1}")

    ax.set_xlabel("Latitude")
    ax.set_ylabel("Longitude")
    ax.set_zlabel("Altitude")
    ax.set_title("Satellite Positions")
    ax.legend()

    if save_path:
        plt.savefig(save_path, format="png")
    else:
        plt.show()


# # Example Usage:
# # Assuming positions_array_lla has shape (num_satellites, num_time_points, 2)
# # Replace 'save_path' with the desired file path if you want to save the graph

# visualize_satellite_positions_2d(positions_array_lla)
