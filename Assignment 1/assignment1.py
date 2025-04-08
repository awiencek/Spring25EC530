import math
from math import sin, cos, acos
import pandas as pd

# Mission of the module:  If the user gives you two arrays of geo location, match each point in the first array to the closest one in the second array

# How to calculate the distance between two GPS locations
# latitude, longitude   (degrees, minutes, seconds)
# Haversine formula (for distance in km)
# D = 6378*arccos[sin(latA)*sin(latB)+cos(latA)*cos(latB)*cos(longA-longB)]

# earth's radius is 6378 km

# function definition: two array inputs, return float output
# array inputs should be structured as follows:
# northern latitudes should be written as positive values, southern as negative values
# eastern longitudes should be written as positive values, western as negative values




def gps_distance(placeA , placeB ):
    'takes two arrays with gps coordinates in degrees and returns the distance in km'
    # convert degrees to radians
    latA = math.radians(placeA[0])
    latB = math.radians(placeB[0])
    longA = math.radians(placeA[1])
    longB = math.radians(placeB[1])

    # calculation for distance
    dist = 6378*acos(sin(latA)*sin(latB)+cos(latA)*cos(latB)*cos(longA-longB))

    return dist


# run the program/function
print("This program will determine the distance between two GPS coordinates")
print("Please input each set of coordinates as an array as such: [latitude, longitude]. Make sure north and east values are positive, while west and south values are negative.")
# place1 = input("Type first coordinate array")
# place2 = input("Type second coordinate array")


def decide_min_geodistance(point, list_of_loc):
    min_distance = gps_distance(point, list_of_loc[0])
    for loc in geo_loc_list:
        distance = gps_distance(loc, point)
        if distance < min_distance:
            min_distance = distance

    print(min_distance)


# Test 1
df = pd.read_csv("boston.csv")
geo_loc_list = df[["latitude", "longitude"]].values.tolist()
current_loc = [42.349220,-71.105751]
decide_min_geodistance(current_loc, geo_loc_list)

# Test 2
# Add logic that iterates through both lists

# Test 3
# Need to add logic that filters/determines/uses different data.

# Test 4
# Need to add logic that filters out mixed-data arrays.

# Test 5
# Need to add logic that filters and works with empty arrays, empty "cells", invalid data(city name, number containing NSEW, etc.)
