import re
import logging
from typing import Tuple

from config import Config

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class Validator:
    """Input validator for address and other inputs"""
    
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)",
        r"(--)|(/\*)|(\*/)",
        r"(\bOR\b.*=)|(\bAND\b.*=)",
        r"(\bUNION\b)",
        r"(;.*--)",
        r"('\s*OR\s*'.*=)",
    ]
    
    @staticmethod
    def validate_address(address: str, field_name: str = "Address") -> str:
        """
        Validate and sanitize an address input
        
        Args:
            address: The address string to validate
            field_name: Name of the field for error messages
            
        Returns:
            Cleaned address string
            
        Raises:
            ValidationError: If validation fails
        """
        if not address or not isinstance(address, str):
            raise ValidationError(f"{field_name} is required and must be a string")
        
        address = address.strip()

        if len(address) < Config.MIN_ADDRESS_LENGTH:
            raise ValidationError(
                f"{field_name} must be at least {Config.MIN_ADDRESS_LENGTH} characters long"
            )
        
        if len(address) > Config.MAX_ADDRESS_LENGTH:
            raise ValidationError(
                f"{field_name} must not exceed {Config.MAX_ADDRESS_LENGTH} characters"
            )
        
        for pattern in Validator.SQL_INJECTION_PATTERNS:
            if re.search(pattern, address, re.IGNORECASE):
                logger.warning(f"Potential SQL injection attempt detected in {field_name}: {address}")
                raise ValidationError(f"{field_name} contains invalid characters")

        if '\x00' in address:
            raise ValidationError(f"{field_name} contains invalid characters")
        
        return address
    
    @staticmethod
    def validate_addresses(source: str, destination: str) -> Tuple[str, str]:
        """
        Validate both source and destination addresses
        
        Args:
            source: Source address
            destination: Destination address
            
        Returns:
            Tuple of (cleaned_source, cleaned_destination)
            
        Raises:
            ValidationError: If validation fails
        """
        cleaned_source = Validator.validate_address(source, "Source address")
        cleaned_destination = Validator.validate_address(destination, "Destination address")
        
        return cleaned_source, cleaned_destination
    
    @staticmethod
    def validate_limit(limit: int, default: int = None) -> int:
        """
        Validate and constrain a limit parameter
        
        Args:
            limit: Requested limit
            default: Default value if limit is invalid
            
        Returns:
            Validated limit value
        """
        default = default or Config.DEFAULT_HISTORY_LIMIT
        
        if not isinstance(limit, int):
            try:
                limit = int(limit)
            except (ValueError, TypeError):
                logger.warning(f"Invalid limit value: {limit}, using default")
                return default
        
        if limit < 1:
            return default
        
        return min(limit, Config.MAX_HISTORY_LIMIT)
    
    @staticmethod
    def validate_coordinates(lat: float, lon: float, location_name: str = "Location") -> Tuple[float, float]:
        """
        Validate latitude and longitude coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            location_name: Name of location for error messages
            
        Returns:
            Tuple of (lat, lon)
            
        Raises:
            ValidationError: If coordinates are invalid
        """
        try:
            lat = float(lat)
            lon = float(lon)
        except (ValueError, TypeError):
            raise ValidationError(f"{location_name} coordinates must be numeric")
        
        if not (-90 <= lat <= 90):
            raise ValidationError(f"{location_name} latitude must be between -90 and 90")
        
        if not (-180 <= lon <= 180):
            raise ValidationError(f"{location_name} longitude must be between -180 and 180")
        
        return lat, lon
