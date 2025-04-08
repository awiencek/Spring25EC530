# geo_distance/__init__.py

"""
geo_distance - A Python package to calculate geographic distances and find the closest locations.
"""

from .geo_calculations import gps_distance, decide_min_geodistance

__all__ = ['gps_distance', 'decide_min_geodistance']

