# First Input:  Your current GPS location
# Second Vector:  Columns AB and  AC of Boston 311 2025  Report (you can find the originals in:  https://data.boston.gov/dataset/311-service-requests)
# Future Bonus:  Find the closest reported issues to your current location.

import pandas as pd
from your_main_code_file import gps_distance, decide_min_geodistance, clean_and_filter_data

# Define your current GPS location (example coordinates for Boston)
current_loc = [42.349220, -71.105751]  # Example: Boston location

# Path to the Boston 311 dataset
dataset_path = "boston_311_2025.csv"  # Replace with the correct path

def test_closest_service_request():
    # Load the Boston 311 dataset
    try:
        df = pd.read_csv(dataset_path)
        
        # Extract only the latitude and longitude columns (AB and AC in your case)
        geo_loc_list = df[["latitude", "longitude"]].values.tolist()

        # Clean the data to remove any invalid coordinates
        geo_loc_list = clean_and_filter_data(geo_loc_list)
        
        # Find the closest service request
        closest_loc, dist = decide_min_geodistance(current_loc, geo_loc_list)
        
        # Output the closest service request and its distance
        print(f"The closest service request to your location ({current_loc}) is at {closest_loc} with a distance of {dist:.2f} km")
        
    except FileNotFoundError:
        print(f"Error: The file '{dataset_path}' was not found.")
    except Exception as e:
        print(f"Error during the test: {e}")

# Run the test
if __name__ == "__main__":
    test_closest_service_request()
