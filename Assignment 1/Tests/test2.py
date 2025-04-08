# Find the closest airport to a city
# First Input:  list of major world cities:  https://raw.githubusercontent.com/joelacus/world-cities/refs/heads/main/world_cities.csv 
# Second Vector:  List of major world airports:  https://github.com/ip2location/ip2location-iata-icao/blob/master/iata-icao.csv
# Future Bonus:  Make your output and input configurables…. Pass a CSV or JSON and get the output as a JSON for the user.
# Why is that?

import pandas as pd
import json
from your_main_code_file import gps_distance, decide_min_geodistance, clean_and_filter_data

# Load the World Cities dataset (CSV format from GitHub)
city_dataset_url = "https://raw.githubusercontent.com/joelacus/world-cities/refs/heads/main/world_cities.csv"
airport_dataset_url = "https://raw.githubusercontent.com/ip2location/ip2location-iata-icao/master/iata-icao.csv"

def load_data(city_url, airport_url):
    """
    Load the city and airport datasets from the provided URLs.
    """
    try:
        cities_df = pd.read_csv(city_url)
        airports_df = pd.read_csv(airport_url)
        return cities_df, airports_df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

def find_closest_airport_to_city(city, airports):
    """
    Find the closest airport to a given city by comparing latitudes and longitudes.
    """
    city_coords = [city["latitude"], city["longitude"]]
    airport_coords = airports[["latitude", "longitude"]].values.tolist()
    
    # Clean the airport data by filtering invalid coordinates
    airport_coords = clean_and_filter_data(airport_coords)
    
    # Find the closest airport
    closest_airport, distance = decide_min_geodistance(city_coords, airport_coords)
    
    return closest_airport, distance

def test_closest_airport():
    """
    Main function to test finding the closest airport for each city.
    """
    cities_df, airports_df = load_data(city_dataset_url, airport_dataset_url)
    
    if cities_df is not None and airports_df is not None:
        results = []
        
        # Iterate over the first few cities (you can adjust this if needed)
        for _, city in cities_df.iterrows():
            closest_airport, distance = find_closest_airport_to_city(city, airports_df)
            
            result = {
                "city": city["city"],
                "country": city["country"],
                "city_coordinates": [city["latitude"], city["longitude"]],
                "closest_airport": closest_airport[0],  # Airport name
                "airport_coordinates": closest_airport[1:],  # Airport latitude, longitude
                "distance_km": distance
            }
            results.append(result)
        
        # Output the results as JSON
        print(json.dumps(results, indent=4))
        
        # Optionally save to a file
        with open("closest_airports.json", "w") as outfile:
            json.dump(results, outfile, indent=4)
    
    else:
        print("Error loading data for cities or airports.")

# Run the test
if __name__ == "__main__":
    test_closest_airport()
