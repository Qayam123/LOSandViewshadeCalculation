import java.io.File;
import java.io.IOException;

import org.gdal.gdal.Band;
import org.gdal.gdal.Dataset;
import org.gdal.gdal.Driver;
import org.gdal.gdal.GCP;
import org.gdal.gdal.gdal;

public class ViewshedCalculator {

    public static void main(String[] args) {
        // Provide the paths to your DEM and output viewshed raster
        String demPath = "path/to/your/dem.tif";
        String outputViewshedPath = "path/to/your/output_viewshed.tif";

        // Observer coordinates (in pixel coordinates, not geographical)
        int observerX = 100;
        int observerY = 100;

        calculateViewshed(demPath, observerX, observerY, outputViewshedPath);
    }

    private static void calculateViewshed(String demPath, int observerX, int observerY, String outputViewshedPath) {
        gdal.AllRegister();

        // Open the DEM dataset
        Dataset demDataset = gdal.Open(demPath);
        if (demDataset == null) {
            System.err.println("Error: Could not open DEM dataset.");
            return;
        }

        // Get the number of rows and columns in the DEM
        int numColumns = demDataset.GetRasterXSize();
        int numRows = demDataset.GetRasterYSize();

        // Create a new dataset for the viewshed
        Driver driver = gdal.GetDriverByName("GTiff");
        Dataset viewshedDataset = driver.Create(outputViewshedPath, numColumns, numRows, 1);

        // Set up the viewshed array
        Band viewshedBand = viewshedDataset.GetRasterBand(1);
        int[] viewshedArray = new int[numColumns * numRows];

        // Iterate through each pixel in the DEM
        for (int row = 0; row < numRows; row++) {
            for (int col = 0; col < numColumns; col++) {
                // Calculate the distance from the observer point to the current pixel
                double distance = Math.sqrt((row - observerY) * (row - observerY) + (col - observerX) * (col - observerX));

                // Check if the pixel is visible based on a simple visibility threshold (e.g., distance < 10)
                if (distance < 10) {
                    viewshedArray[row * numColumns + col] = 255; // Mark pixel as visible
                }
            }
        }

        // Write the viewshed array to the raster dataset
        viewshedBand.WriteRaster(0, 0, numColumns, numRows, viewshedArray);

        // Close datasets
        demDataset.delete();
        viewshedDataset.delete();
    }
}

