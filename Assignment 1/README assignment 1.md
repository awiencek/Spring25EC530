GPS Distance Calculator
Mission
This Python script calculates the distance between two GPS coordinates, given as arrays of latitude and longitude. The script finds the closest match between two sets of geographical points using the Haversine formula for calculating distance in kilometers.

How it Works
The script uses the Haversine formula to calculate the distance between two geographical points on the Earth's surface. The formula is as follows:

𝐷
=
6378
×
arccos
⁡
(
sin
⁡
(
latA
)
×
sin
⁡
(
latB
)
+
cos
⁡
(
latA
)
×
cos
⁡
(
latB
)
×
cos
⁡
(
longA
−
longB
)
)
D=6378×arccos(sin(latA)×sin(latB)+cos(latA)×cos(latB)×cos(longA−longB))
Where:

𝐷
D is the distance in kilometers.

Latitude and longitude are in degrees (converted to radians for calculation).

The Earth's radius is assumed to be 6378 km.

Input Format
You need to provide two arrays, each containing the latitude and longitude of a location. The format for each array is as follows:

python
Copy
[latitude, longitude]
Latitude: Northern latitudes are positive, and southern latitudes are negative.

Longitude: Eastern longitudes are positive, and western longitudes are negative.

Example
python
Copy
place1 = [40.7128, -74.0060]  # New York City (latitude, longitude)
place2 = [34.0522, -118.2437] # Los Angeles (latitude, longitude)
Function Definition
python
Copy
def gps_distance(placeA, placeB):
    """
    Takes two arrays with GPS coordinates in degrees (latitude, longitude)
    and returns the distance in kilometers.
    """
Parameters:
placeA: An array of the first location's [latitude, longitude] in degrees.

placeB: An array of the second location's [latitude, longitude] in degrees.

Returns:
A float representing the distance between the two points in kilometers.

How to Use
Run the script.

Input the GPS coordinates as arrays when prompted.

The script will print the distance between the two locations in kilometers.

Example Output
bash
Copy
This program will determine the distance between two GPS coordinates
Please input each set of coordinates as an array as such: [latitude, longitude]. Make sure north and east values are positive, while west and south values are negative.
Type first coordinate array [40.7128, -74.0060]
Type second coordinate array [34.0522, -118.2437]
Distance: 3936.09 km
Notes
Ensure that the coordinates are correctly formatted and that the northern and eastern values are positive, while the southern and western values are negative.

The script uses radians for trigonometric calculations, converting degrees to radians as needed.

Requirements
Python 3.x

math library (built-in)

License
This script is open-source and free to use and modify.
