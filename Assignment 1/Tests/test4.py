# Study the following files...
# https://drive.google.com/file/d/1B5OVEcLH0iM23DDqc2PlGGPhTl5xmw77/view?usp=sharing
# https://drive.google.com/file/d/1Iw3MJxakfyIUzK21GpEoOtHBFmYuqrX6/view?usp=sharing 

# What did you learn?

# First input is: one of the files
# Second Vector:  List of major world airports:  https://github.com/ip2location/ip2location-iata-icao/blob/master/iata-icao.csv

import pandas as pd
import json
from your_main_code_file import gps_distance, decide_min_geodistance, clean_and_filter_data

# Load the airports dataset
def load_airports_data(airport_url):
    """
    Load the airports dataset from a CSV URL.
    """
    try:
        airports_df = pd.read_csv(airport_url)
        return airports_df
    except Exception as e:
        print(f"Error loading airports data: {e}")
        return None

# Load the user-provided file (CSV or Excel)
def load_input_file(file_path):
    """
    Load the input file, either CSV or Excel, based on the file extension.
    """
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return pd.read_excel(file_path)
        else:
            print("Unsupported file format.")
            return None
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

# Analyze the structure of the loaded file (columns, first rows)
def analyze_file_structure(df):
    """
    Analyze the structure of the provided file.
    """
    if df is not None:
        print("File Structure:")
        print(f"Columns: {df.columns}")
        print(f"First 5 rows:\n{df.head()}")
    else:
        print("Invalid file data.")

# Find the closest airport to a given location
def find_closest_airport_to_location(location, airports_df):
    """
    Find the closest airport to the location based on latitude and longitude.
    """
    location_coords = [location["Latitude"], location["Longitude"]]
    airport_coords = airports_df[["latitude", "longitude"]].values.tolist()
    
    # Clean the airport data by filtering invalid coordinates
    airport_coords = clean_and_filter_data(airport_coords)
    
    # Find the closest airport
    closest_airport, distance = decide_min_geodistance(location_coords, airport_coords)
    
    return closest_airport, distance

def test_file_analysis():
    """
    Main function to analyze the input file and compare with the airports dataset.
    """
    # Load the airports data
    airport_url = "https://raw.githubusercontent.com/ip2location/ip2location-iata-icao/master/iata-icao.csv"
    airports_df = load_airports_data(airport_url)
    
    if airports_df is not None:
        # Path to the user-provided file (you can change this path)
        file_path = "path_to_downloaded_file.csv"  # Change this to the actual path of the downloaded file
        
        # Load the user input file
        input_df = load_input_file(file_path)
        
        # Analyze the file structure (print out the columns and first rows)
        analyze_file_structure(input_df)
        
        if input_df is not None:
            results = []
            
            # Assuming the input file contains columns 'Latitude' and 'Longitude' for location
            for _, location in input_df.iterrows():
                # Find the closest airport to the given location
                closest_airport, dist = find_closest_airport_to_location(location, airports_df)
                
                result = {
                    "location_name": location.get("Place Name", "N/A"),  # Assuming 'Place Name' column exists
                    "location_coordinates": [location.get("Latitude"), location.get("Longitude")],
                    "closest_airport": closest_airport[0],  # Airport name
                    "airport_coordinates": closest_airport[1:],  # Airport latitude, longitude
                    "distance_km": dist
                }
                results.append(result)
            
            # Output the results as JSON
            print(json.dumps(results, indent=4))
            
            # Optionally, save to a file
            with open("closest_airports_from_file_analysis.json", "w") as outfile:
                json.dump(results, outfile, indent=4)
                
        else:
            print("Error: Invalid file data.")
    
    else:
        print("Error loading airports data.")

# Run the test
if __name__ == "__main__":
    test_file_analysis()
