#!/usr/bin/env python

import rasterio
from rasterio.enums import Resampling
import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_line_of_sight(input_dem_path, observer_location, output_line_of_sight_path):
    # Open the DEM dataset
    with rasterio.open(input_dem_path) as dem_dataset:
        # Read the DEM data as a NumPy array
        dem_data = dem_dataset.read(1)

        # Get the geotransform information
        transform = dem_dataset.transform

        # Get the row and column indices of the observer point
        observer_col, observer_row = ~transform * observer_location

        # Set up the line-of-sight array
        line_of_sight = np.zeros_like(dem_data, dtype=np.uint8)

        # Iterate through each pixel in the DEM
        for row in range(dem_data.shape[0]):
            for col in range(dem_data.shape[1]):
                # Calculate the distance from the observer point to the current pixel
                distance = np.sqrt((row - observer_row)**2 + (col - observer_col)**2)

                # Check if the pixel is within the line of sight based on a simple threshold (e.g., distance < 10)
                if distance < 100:
                    line_of_sight[row, col] = 255  # Mark pixel as within line of sight

        # Write the line-of-sight array to a new GeoTIFF file
        with rasterio.open(output_line_of_sight_path, 'w', driver='GTiff',
                           height=dem_data.shape[0], width=dem_data.shape[1],
                           count=1, dtype=np.uint8, crs=dem_dataset.crs,
                           transform=transform) as dst:
            dst.write(line_of_sight, 1)

if __name__ == "__main__":
    # Example usage
    dem_path = "data.tif"
    observer_location = (325000, 515000)  # Example observer point in UTM coordinates
    output_line_of_sight_path = "LOS.tif"
    os.system("gdal_viewshed -md 20000 -ox 325000 -oy 515000 -oz 1.5 -tz 200 data.tif viewshade.tif")

    calculate_line_of_sight(dem_path, observer_location, output_line_of_sight_path)

