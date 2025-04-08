# additional input problems/errors users can encounter

#additional things that can be tested
#csv with missing data cells
#mixed input units
#output units
#extra characters (direction, units, etc) in input data
#non number input
#improper array formatting

import pandas as pd
import math
import re
import json
from your_main_code_file import gps_distance, decide_min_geodistance, clean_and_filter_data

# Function to clean and convert mixed input units
def clean_coordinates(coordinate):
    """
    Cleans the coordinates by removing extra characters (NSEW) and converting units if necessary.
    """
    # Remove extra characters like N/S/E/W and strip spaces
    coordinate = coordinate.strip().upper()
    
    # If the coordinate contains NSEW, remove it (we'll assume positive is north/east, negative is south/west)
    coordinate = re.sub(r'[NSEW]', '', coordinate)
    
    # Convert to float if it's a valid number
    try:
        coordinate = float(coordinate)
    except ValueError:
        raise ValueError(f"Invalid coordinate format: {coordinate}")
    
    return coordinate

# Function to check and handle missing data cells in the CSV
def handle_missing_data(df):
    """
    Checks for missing data in the dataframe and handles it by either filling or skipping rows.
    """
    if df.isnull().values.any():
        print("Warning: Missing data found in the file. These rows will be skipped.")
        # Drop rows with missing latitude or longitude
        df = df.dropna(subset=['Latitude', 'Longitude'])
    return df

# Function to handle mixed input units (Degrees to Radians conversion)
def convert_to_radians(degrees):
    """
    Converts degrees to radians.
    """
    return math.radians(degrees)

# Function to check for non-numeric input and clean improperly formatted arrays
def validate_and_clean_input(df):
    """
    Validates and cleans the input data (ensures it's numeric, removes extra characters, and handles improper array formatting).
    """
    for index, row in df.iterrows():
        # Check if latitude and longitude are numeric
        try:
            lat = clean_coordinates(row['Latitude'])
            long = clean_coordinates(row['Longitude'])
        except ValueError as e:
            print(f"Skipping row {index} due to error: {e}")
            df = df.drop(index)
            continue
        
        # Optional: Convert to radians for calculation
        row['Latitude'] = convert_to_radians(lat)
        row['Longitude'] = convert_to_radians(long)
    
    return df

# Main function to test various input issues
def test_input_errors(file_path, airport_url):
    """
    Main function to handle input errors such as missing data, non-numeric input, and improper array formatting.
    """
    try:
        # Load the airports data
        airports_df = pd.read_csv(airport_url)
        if airports_df is None:
            print("Error loading airports data.")
            return
        
        # Load the user input file (CSV)
        df = pd.read_csv(file_path)
        
        # Handle missing data by dropping rows with missing latitude/longitude
        df = handle_missing_data(df)
        
        # Validate and clean the input data
        df = validate_and_clean_input(df)
        
        results = []
        
        # Iterate over cleaned data and find the closest airport
        for _, location in df.iterrows():
            # Find the closest airport
            closest_airport, dist = decide_min_geodistance([location['Latitude'], location['Longitude']], airports_df[['latitude', 'longitude']].values.tolist())
            
            result = {
                "location_name": location.get("Place Name", "N/A"),  # Assuming a column for place name exists
                "location_coordinates": [location['Latitude'], location['Longitude']],
                "closest_airport": closest_airport[0],  # Airport name
                "airport_coordinates": closest_airport[1:],  # Airport coordinates (latitude, longitude)
                "distance_km": dist
            }
            results.append(result)
        
        # Output the results as JSON
        print(json.dumps(results, indent=4))
        
        # Optionally, save the results to a file
        with open("cleaned_closest_airports.json", "w") as outfile:
            json.dump(results, outfile, indent=4)
    
    except Exception as e:
        print(f"Error during the test: {e}")

# Run the test with input errors
if __name__ == "__main__":
    test_input_errors("path_to_input_file.csv", "https://raw.githubusercontent.com/ip2location/ip2location-iata-icao/master/iata-icao.csv")
