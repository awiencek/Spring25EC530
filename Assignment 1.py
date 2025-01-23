#please go to https://github.com/awiencek/Spring25EC530/blob/main/Assignment%201/assignment1.py to see updated/better tested code for this assignment and its readme file



import math
from math import sin, cos, acos

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


def gps_distance(placeA array, placeB array):
    'takes two arrays with gps coordinates in degrees and returns the distance in km'
    # convert degrees to radians
    latA = math.radians(placeA[0])
    latB = math.radians(placeB[0])
    longA = math.radians(placeA[1])
    longB = math.radians(placeB[1])

    # calculation for distance
    dist = 6378*acos[sin(latA)*sin(latB)+cos(latA)*cos(latB)*cos(longA-longB)]

    return dist


# run the program/function
print("This program will determine the distance between two GPS coordinates")
print("Please input each set of coordinates as an array as such: [latitude, longitude]. Make sure north and east values are positive, while west and south values are negative.")
place1 = input("Type first coordinate array")
place2 = input("Type second coordinate array")

distance = gps_distance(place1, place2)
print(distance, " km")
