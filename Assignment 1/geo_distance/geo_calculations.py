

import math
import pandas as pd

# Mission of the module: If the user gives two arrays of geo location, match each point in the first array to the closest one in the second array

# How to calculate the distance between two GPS locations
# Latitude, longitude (degrees, minutes, seconds)
# Haversine formula (for distance in km)
# D = 6378 * arccos[sin(latA)*sin(latB) + cos(latA)*cos(latB)*cos(longA-longB)]

# Earth's radius is 6378 km

# Function to calculate the distance between two GPS coordinates
def gps_distance(placeA, placeB):
    """Takes two arrays with gps coordinates in degrees and returns the distance in km"""
    try:
        # Convert degrees to radians
        latA = math.radians(placeA[0])
        latB = math.radians(placeB[0])
        longA = math.radians(placeA[1])
        longB = math.radians(placeB[1])

        # Calculation for distance
        dist = 6378 * math.acos(math.sin(latA) * math.sin(latB) + math.cos(latA) * math.cos(latB) * math.cos(longA - longB))
        return dist
    except Exception as e:
        print(f"Error calculating distance: {e}")
        return float('inf')  # Return an infinite distance if there's an error

# Function to find the closest location
def decide_min_geodistance(point, list_of_loc):
    """Takes a point and a list of locations, returns the closest point and distance"""
    min_distance = float('inf')
    closest_location = None
    
    for loc in list_of_loc:
        distance = gps_distance(loc, point)
        if distance < min_distance:
            min_distance = distance
            closest_location = loc
            
    return closest_location, min_distance

# Function to filter out invalid GPS data
def is_valid_coordinate(coord):
    """Checks if a coordinate array has valid latitude and longitude"""
    if isinstance(coord, list) and len(coord) == 2:
        lat, lon = coord
        return -90 <= lat <= 90 and -180 <= lon <= 180
    return False

# Function to clean and filter the data
def clean_and_filter_data(data):
    """Removes rows with invalid coordinates and empty cells"""
    valid_data = []
    for coord in data:
        if is_valid_coordinate(coord):
            valid_data.append(coord)
        else:
            print(f"Invalid coordinate skipped: {coord}")
    return valid_data

# Test 1: Using a CSV of GPS coordinates
def test_with_csv(csv_file, current_loc):
    df = pd.read_csv(csv_file)
    geo_loc_list = df[["latitude", "longitude"]].values.tolist()
    
    # Clean the data
    geo_loc_list = clean_and_filter_data(geo_loc_list)
    
    # Find the closest location
    closest_loc, dist = decide_min_geodistance(current_loc, geo_loc_list)
    print(f"The closest location to {current_loc} is {closest_loc} with a distance of {dist:.2f} km")

# Example usage:
if __name__ == "__main__":
    print("This program will determine the distance between two GPS coordinates.")
    current_loc = [42.349220, -71.105751]  # Example: Boston location
    csv_file = "boston.csv"  # Replace with your actual CSV file path
    
    # Test with a CSV of coordinates
    test_with_csv(csv_file, current_loc)
