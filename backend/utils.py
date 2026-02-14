"""
Utilities module
Helper functions for distance calculations and conversions
"""

from math import radians, cos, sin, asin, sqrt
import logging

from config import Config

logger = logging.getLogger(__name__)


class DistanceCalculator:
    """Calculator for geographic distances"""
    
    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points on Earth
        using the Haversine formula
        
        Args:
            lat1: Latitude of first point (decimal degrees)
            lon1: Longitude of first point (decimal degrees)
            lat2: Latitude of second point (decimal degrees)
            lon2: Longitude of second point (decimal degrees)
            
        Returns:
            Distance in kilometers
        """
        # Convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        # Distance in kilometers
        distance = c * Config.EARTH_RADIUS_KM
        
        logger.debug(f"Calculated distance: {distance:.2f} km between ({lat1}, {lon1}) and ({lat2}, {lon2})")
        
        return distance
    
    @staticmethod
    def km_to_miles(km: float) -> float:
        """
        Convert kilometers to miles
        
        Args:
            km: Distance in kilometers
            
        Returns:
            Distance in miles
        """
        return km * Config.KM_TO_MILES_FACTOR
    
    @staticmethod
    def miles_to_km(miles: float) -> float:
        """
        Convert miles to kilometers
        
        Args:
            miles: Distance in miles
            
        Returns:
            Distance in kilometers
        """
        return miles / Config.KM_TO_MILES_FACTOR
    
    @staticmethod
    def calculate_distance_between_addresses(
        source_coords: dict,
        dest_coords: dict
    ) -> dict:
        """
        Calculate distance between two address coordinates
        
        Args:
            source_coords: Dictionary with 'lat' and 'lon' keys
            dest_coords: Dictionary with 'lat' and 'lon' keys
            
        Returns:
            Dictionary with 'km' and 'miles' keys
        """
        distance_km = DistanceCalculator.haversine_distance(
            source_coords['lat'],
            source_coords['lon'],
            dest_coords['lat'],
            dest_coords['lon']
        )
        
        distance_miles = DistanceCalculator.km_to_miles(distance_km)
        
        return {
            'km': round(distance_km, 2),
            'miles': round(distance_miles, 2)
        }


class ResponseFormatter:
    """Formatter for API responses"""
    
    @staticmethod
    def format_distance_response(
        source: str,
        destination: str,
        source_coords: dict,
        dest_coords: dict,
        distance_km: float,
        distance_miles: float
    ) -> dict:
        """
        Format a distance calculation response
        
        Args:
            source: Source address
            destination: Destination address
            source_coords: Source coordinates
            dest_coords: Destination coordinates
            distance_km: Distance in kilometers
            distance_miles: Distance in miles
            
        Returns:
            Formatted response dictionary
        """
        return {
            'source': source,
            'destination': destination,
            'distance_km': round(distance_km, 2),
            'distance_miles': round(distance_miles, 2),
            'source_coords': source_coords,
            'destination_coords': dest_coords
        }
    
    @staticmethod
    def format_error_response(error_message: str, status_code: int = 400) -> tuple:
        """
        Format an error response
        
        Args:
            error_message: Error message
            status_code: HTTP status code
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        return {'error': error_message}, status_code
    
    @staticmethod
    def format_success_response(data: dict, status_code: int = 200) -> tuple:
        """
        Format a success response
        
        Args:
            data: Response data
            status_code: HTTP status code
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        return data, status_code
    
    @staticmethod
    def format_history_response(queries: list) -> dict:
        """
        Format a history response
        
        Args:
            queries: List of query dictionaries
            
        Returns:
            Formatted response dictionary
        """
        return {
            'queries': queries,
            'count': len(queries)
        }
