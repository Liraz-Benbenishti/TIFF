import numpy as np
import rasterio
import argparse
import sys

def compare_tiff_files(original_file, reconstructed_file, threshold_cm=1):
    # Open the original GeoTIFF file
    with rasterio.open(original_file) as src1:
        original_data = src1.read(1)
    
    # Open the reconstructed GeoTIFF file
    with rasterio.open(reconstructed_file) as src2:
        reconstructed_data = src2.read(1)
    
    # Check if dimensions match
    if original_data.shape != reconstructed_data.shape:
        print("Error: The dimensions of the two files do not match.")
        return 1
    
    # Calculate the absolute differences
    differences = np.abs(original_data - reconstructed_data)
    
    # Check if any difference exceeds the threshold in meters (1 cm = 0.01 meters)
    if np.any(differences > (threshold_cm / 100.0)):
        return 1
    else:
        return 0

def main():
    parser = argparse.ArgumentParser(description='Compare two GeoTIFF files.')
    parser.add_argument('original_file', type=str, help='Path to the original GeoTIFF file')
    parser.add_argument('reconstructed_file', type=str, help='Path to the reconstructed GeoTIFF file')
    parser.add_argument('--threshold', type=float, default=1.0, help='Threshold in centimeters for the maximum allowed difference (default: 1 cm)')

    args = parser.parse_args()

    result = compare_tiff_files(args.original_file, args.reconstructed_file, args.threshold)
    sys.exit(result)

if __name__ == "__main__":
    main()
