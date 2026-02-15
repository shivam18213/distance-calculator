import requests
import logging
from typing import Dict, Optional

from config import Config

logger = logging.getLogger(__name__)


class GeocodingError(Exception):
    """Custom exception for geocoding errors"""
    pass


class Geocoder:
    """Geocoder using Nominatim (OpenStreetMap) API"""
    
    def __init__(self):
        """Initialize geocoder with configuration"""
        self.base_url = Config.NOMINATIM_BASE_URL
        self.timeout = Config.NOMINATIM_TIMEOUT
        self.headers = {
            'User-Agent': Config.NOMINATIM_USER_AGENT
        }
    
    def geocode(self, address: str) -> Dict[str, float]:
        """
        Geocode an address to coordinates
        
        Args:
            address: Address string to geocode
            
        Returns:
            Dictionary with 'lat' and 'lon' keys
            
        Raises:
            GeocodingError: If geocoding fails
        """
        logger.info(f"Geocoding address: {address}")
        
        try:
            url = f"{self.base_url}/search"
            params = {
                'q': address,
                'format': 'json',
                'limit': 1
            }
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            if not data:
                logger.warning(f"No results found for address: {address}")
                raise GeocodingError(f"Could not find address: {address}")
            
            result = data[0]
            lat = float(result['lat'])
            lon = float(result['lon'])
            
            logger.info(f"Successfully geocoded: {address} -> ({lat}, {lon})")
            
            return {'lat': lat, 'lon': lon}
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout while geocoding address: {address}")
            raise GeocodingError("Geocoding service timed out. Please try again.")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error while geocoding {address}: {str(e)}")
            raise GeocodingError("Failed to connect to geocoding service")
        
        except (KeyError, ValueError, IndexError) as e:
            logger.error(f"Error parsing geocoding response for {address}: {str(e)}")
            raise GeocodingError("Invalid geocoding response")
    
    def reverse_geocode(self, lat: float, lon: float) -> Optional[str]:
        """
        Reverse geocode coordinates to an address
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Address string or None if not found
        """
        logger.info(f"Reverse geocoding coordinates: ({lat}, {lon})")
        
        try:
            url = f"{self.base_url}/reverse"
            params = {
                'lat': lat,
                'lon': lon,
                'format': 'json'
            }
            
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            if 'display_name' in data:
                address = data['display_name']
                logger.info(f"Reverse geocoded: ({lat}, {lon}) -> {address}")
                return address
            
            return None
            
        except Exception as e:
            logger.error(f"Error reverse geocoding ({lat}, {lon}): {str(e)}")
            return None
    
    def batch_geocode(self, addresses: list) -> Dict[str, Dict[str, float]]:
        """
        Geocode multiple addresses
        
        Args:
            addresses: List of address strings
            
        Returns:
            Dictionary mapping addresses to coordinates
        """
        results = {}
        
        for address in addresses:
            try:
                coords = self.geocode(address)
                results[address] = coords
            except GeocodingError as e:
                logger.warning(f"Failed to geocode {address}: {str(e)}")
                results[address] = None
        
        return results
