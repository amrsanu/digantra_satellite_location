# Satellite Positioning Project

## Overview

This repository contains scripts and utilities for computing and analyzing satellite positions. The project involves using Two-Line Element (TLE) data, satellite propagation, coordinate conversion, and filtering based on user-defined regions.

## Contents

- **satellite.py.py**: Main script for computing satellite positions and filtering based on regions.
- **satellite_utils.py**: Utilities for working with TLE data and computing satellite positions.
- **visualization_utils.py**: (Optional) Utilities for visualizing satellite positions.
- **requirements.txt**: List of Python dependencies.

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/amrsanu/digantra_satellite_location.git
   cd digantra_satellite_location
   ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the main script:

    ```bash
    python main_script.py
    ```

4. Usage

    - main_script.py reads TLE data, computes satellite positions, and filters results based on user-defined regions.
    - Modify TLE_FILE_PATH, DAYS, TIME_INTERVAL, and CORNER_POINTS in main_script.py for customization.
    - (Optional) Use visualization_utils.py for visualizing satellite positions.

5. Performance Optimization

    - The script uses multi-threading for parallel computation.
    - Consider exploring distributed computing frameworks for larger datasets.
    - GPU acceleration can be explored for faster computation (update script accordingly).