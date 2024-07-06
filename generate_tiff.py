import numpy as np
import rasterio
from rasterio.transform import from_origin
import random
import noise

def generate_perlin_noise(width, height, scale=100):
    data = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            data[y][x] = noise.pnoise2(x / scale, 
                                       y / scale, 
                                       octaves=6, 
                                       persistence=0.5, 
                                       lacunarity=2.0, 
                                       repeatx=1024, 
                                       repeaty=1024, 
                                       base=0)
    return data

def add_continuous_nodata_areas(data, nodata_value=-10000, max_areas=8):
    height, width = data.shape
    num_areas = random.randint(1, max_areas)
    
    for _ in range(num_areas):
        # Generate a random valley or mountain that is approximately 4000 pixels wide
        feature_width = 4000  # 4000 pixels wide, corresponds to about 400 meters
        start_x = random.randint(0, width - feature_width)
        end_x = start_x + feature_width
        
        # Randomly determine if it's a valley or mountain
        is_valley = random.choice([True, False])
        if is_valley:
            valley_depth = random.uniform(0.2, 0.5)  # Depth of the valley relative to the height range
            for x in range(start_x, end_x):
                valley_bottom = random.uniform(0.2, 0.4)  # Bottom of the valley relative to the height range
                for y in range(height):
                    data[y][x] -= valley_depth * np.sin((x - start_x) * np.pi / feature_width) + valley_bottom
        else:
            mountain_height = random.uniform(0.5, 1.0)  # Height of the mountain relative to the height range
            for x in range(start_x, end_x):
                mountain_peak = random.uniform(0.6, 0.8)  # Peak of the mountain relative to the height range
                for y in range(height):
                    data[y][x] += mountain_height * np.sin((x - start_x) * np.pi / feature_width) + mountain_peak
        
    return data

def generate_random_geotiff():
    # Generate random dimensions for the image within the specified range
    width = random.randint(6000, 2\40000)
    height = random.randint(6000, 40000)
    
    # Generate Perlin noise data
    scale = random.uniform(50, 150)
    data = generate_perlin_noise(width, height, scale)
    
    # Normalize the data to a specific range, e.g., 0 to 1000 meters
    min_height = 0
    max_height = 1000
    normalized_data = min_height + (max_height - min_height) * (data - np.min(data)) / np.ptp(data)
    
    # Add continuous nodata areas
    nodata_value = -10000
    data_with_nodata = add_continuous_nodata_areas(normalized_data, nodata_value, max_areas=8)
    
    # Define the geospatial transform
    transform = from_origin(0, 0, 1, 1)  # (top-left-x, top-left-y, pixel-width, pixel-height)
    
    # Define the metadata
    metadata = {
        'driver': 'GTiff',
        'dtype': 'float32',
        'nodata': nodata_value,
        'width': width,
        'height': height,
        'count': 1,
        'crs': 'EPSG:4326',  # WGS84 coordinate system
        'transform': transform
    }
    
    # Write the data to a GeoTIFF file
    output_file = f'random_height_map_with_nodata_{width}x{height}.tif'
    with rasterio.open(output_file, 'w', **metadata) as dst:
        dst.write(data_with_nodata.astype(np.float32), 1)
    
    print(f"Generated a {width}x{height} GeoTIFF file named '{output_file}' with valleys and mountains")

# Generate the random GeoTIFF file
generate_random_geotiff()
