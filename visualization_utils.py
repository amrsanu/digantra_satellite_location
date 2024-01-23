# visualization_utils.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def visualize_satellite_positions(positions_array, save_path=None):
    """
    Visualize satellite positions over time in a 3D space with different colors for each satellite.

    Parameters:
    - positions_array (numpy.ndarray): 3D array containing positions for each satellite at each time point.
    - save_path (str): Optional. If provided, the graph will be saved at the specified path.
    """
    num_satellites, num_time_points, _ = positions_array.shape

    # Create a list of unique colors for each satellite
    colors = plt.cm.viridis(np.linspace(0, 1, num_satellites))

    # Plot 3D graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    for i in range(num_satellites):
        x = positions_array[i, :, 0]
        y = positions_array[i, :, 1]
        z = positions_array[i, :, 2]

        ax.plot(x, y, z, color=colors[i], label=f"Satellite {i+1}")

    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.set_zlabel("Z (km)")
    ax.set_title("Satellite Positions")
    ax.legend()

    if save_path:
        plt.savefig(save_path, format="png")
    else:
        plt.show()
