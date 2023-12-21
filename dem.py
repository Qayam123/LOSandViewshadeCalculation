from osgeo import gdal

def get_dem_extent(tif_path):
    # Open the DEM dataset
    dem_dataset = gdal.Open(tif_path)

    if not dem_dataset:
        print("Error: Could not open DEM dataset.")
        return None

    # Get the geotransform information
    geotransform = dem_dataset.GetGeoTransform()

    # Check the length of the geotransform tuple
    if len(geotransform) != 6:
        print("Error: Unexpected geotransform format.")
        return None

    x_origin, x_pixel_size, _, y_origin, _, y_pixel_size = geotransform

    # Get the number of rows and columns
    num_columns = dem_dataset.RasterXSize
    num_rows = dem_dataset.RasterYSize

    # Calculate the extent of the DEM
    min_x = x_origin
    max_x = x_origin + num_columns * x_pixel_size
    min_y = y_origin + num_rows * y_pixel_size
    max_y = y_origin

    # Close the dataset
    dem_dataset = None

    return min_x, min_y, max_x, max_y

if __name__ == "__main__":
    # Example usage
    dem_path = "data.tif"

    dem_extent = get_dem_extent(dem_path)

    if dem_extent:
        print(f"DEM Extent: {dem_extent}")


