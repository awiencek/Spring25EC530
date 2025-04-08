# First input is:
# https://docs.google.com/spreadsheets/d/1oJy_VQ08Fjdj-hwMXYTR0dUTlrahBTyPRlJQrjuK9ZE/edit?usp=sharing 
# Second Vector:  List of major world airports: 
# https://github.com/ip2location/ip2location-iata-icao/blob/master/iata-icao.csv

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from your_main_code_file import gps_distance, decide_min_geodistance, clean_and_filter_data
import json

# Google Sheets API authentication
def authenticate_google_sheets(credentials_file):
    """
    Authenticate with Google Sheets API using a service account.
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)
    return client

def load_google_sheet_data(sheet_url, client):
    """
    Load data from the Google Spreadsheet.
    """
    # Open the Google Spreadsheet by URL
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)  # Assuming the first worksheet contains the data
    data = worksheet.get_all_records()  # Get all data as a list of dictionaries
    return data

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

def find_closest_airport_to_location(location, airports):
    """
    Find the closest airport to a given location by comparing latitudes and longitudes.
    """
    location_coords = [location["latitude"], location["longitude"]]
    airport_coords = airports[["latitude", "longitude"]].values.tolist()
    
    # Clean the airport data by filtering invalid coordinates
    airport_coords = clean_and_filter_data(airport_coords)
    
    # Find the closest airport
    closest_airport, distance = decide_min_geodistance(location_coords, airport_coords)
    
    return closest_airport, distance

def test_closest_airport_from_google_sheet():
    """
    Main function to test finding the closest airport from locations in a Google Sheet.
    """
    # Google Sheet URL and authentication credentials
    sheet_url = "https://docs.google.com/spreadsheets/d/1oJy_VQ08Fjdj-hwMXYTR0dUTlrahBTyPRlJQrjuK9ZE/edit?usp=sharing"
    credentials_file = "path_to_your_credentials_file.json"  # Path to your Google API credentials JSON file
    
    try:
        # Authenticate and load data
        client = authenticate_google_sheets(credentials_file)
        locations_data = load_google_sheet_data(sheet_url, client)
        
        # Load the airports data from the URL
        airport_url = "https://raw.githubusercontent.com/ip2location/ip2location-iata-icao/master/iata-icao.csv"
        airports_df = load_airports_data(airport_url)
        
        if airports_df is not None:
            results = []
            
            # Iterate through each location from the Google Sheets data
            for location in locations_data:
                closest_airport, dist = find_closest_airport_to_location(location, airports_df)
                
                result = {
                    "location_name": location.get("Place Name", "N/A"),  # Assuming column for place name
                    "location_coordinates": [location.get("Latitude"), location.get("Longitude")],
                    "closest_airport": closest_airport[0],  # Airport name
                    "airport_coordinates": closest_airport[1:],  # Airport latitude, longitude
                    "distance_km": dist
                }
                results.append(result)
            
            # Output the results as JSON
            print(json.dumps(results, indent=4))
            
            # Optionally, save to a file
            with open("closest_airports_from_google_sheet.json", "w") as outfile:
                json.dump(results, outfile, indent=4)
                
        else:
            print("Error loading airports data.")
    
    except Exception as e:
        print(f"Error during the test: {e}")

# Run the test
if __name__ == "__main__":
    test_closest_airport_from_google_sheet()
