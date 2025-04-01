# GPS Distance Calculator

## Mission

This Python script calculates the distance between two GPS coordinates, given as arrays of latitude and longitude. The script finds the closest match between two sets of geographical points using the Haversine formula for calculating distance in kilometers.

## How it Works

The script uses the Haversine formula to calculate the distance between two geographical points on the Earth's surface. The formula is as follows:

\[
D = 6378 \times \arccos \left( \sin (\text{latA}) \times \sin (\text{latB}) + \cos (\text{latA}) \times \cos (\text{latB}) \times \cos (\text{longA} - \text{longB}) \right)
\]

Where:

- \(D\) is the distance in kilometers.
- Latitude and longitude are in degrees (converted to radians for calculation).
- The Earth's radius is assumed to be 6378 km.

## Input Format

You need to provide two arrays, each containing the latitude and longitude of a location. The format for each array is as follows:

```python
[latitude, longitude]

# Example
place1 = [40.7128, -74.0060]  # New York City (latitude, longitude)
place2 = [34.0522, -118.2437]  # Los Angeles (latitude, longitude)

# Notes
Ensure that the coordinates are correctly formatted and that the northern and eastern values are positive, while the southern and western values are negative.

The script uses radians for trigonometric calculations, converting degrees to radians as needed.

## Requirements
Python 3.x

math library (built-in)

## License
This script is open-source and free to use and modify.
