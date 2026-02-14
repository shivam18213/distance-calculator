import pytest
from validation import Validator, ValidationError
from utils import DistanceCalculator
from geocoding import Geocoder, GeocodingError


class TestValidator:
    
    def test_valid_address(self):
        """Test valid address validation"""
        address = Validator.validate_address("New York, NY")
        assert address == "New York, NY"
    
    def test_empty_address(self):
        """Test empty address validation"""
        with pytest.raises(ValidationError):
            Validator.validate_address("")
    
    def test_address_too_short(self):
        """Test address that's too short"""
        with pytest.raises(ValidationError):
            Validator.validate_address("NY")
    
    def test_address_too_long(self):
        """Test address that's too long"""
        with pytest.raises(ValidationError):
            Validator.validate_address("x" * 300)
    
    def test_sql_injection_detection(self):
        """Test SQL injection pattern detection"""
        with pytest.raises(ValidationError):
            Validator.validate_address("SELECT * FROM users")
        
        with pytest.raises(ValidationError):
            Validator.validate_address("DROP TABLE queries")
        
        with pytest.raises(ValidationError):
            Validator.validate_address("' OR '1'='1")
    
    def test_whitespace_trimming(self):
        """Test that whitespace is trimmed"""
        address = Validator.validate_address("  Paris, France  ")
        assert address == "Paris, France"
    
    def test_validate_addresses(self):
        """Test validating both addresses"""
        source, dest = Validator.validate_addresses("NYC", "LA")
        assert source == "NYC"
        assert dest == "LA"
    
    def test_validate_coordinates(self):
        """Test coordinate validation"""
        lat, lon = Validator.validate_coordinates(40.7, -74.0)
        assert lat == 40.7
        assert lon == -74.0
        
        # Invalid latitude
        with pytest.raises(ValidationError):
            Validator.validate_coordinates(100, 0)
        
        # Invalid longitude
        with pytest.raises(ValidationError):
            Validator.validate_coordinates(0, 200)


class TestDistanceCalculator:
    """Test distance calculation utilities"""
    
    def test_haversine_distance(self):
        """Test Haversine distance calculation"""
        # Distance between NYC and LA (approximately 3944 km)
        distance = DistanceCalculator.haversine_distance(
            40.7128, -74.0060,  # NYC
            34.0522, -118.2437  # LA
        )
        assert 3900 < distance < 4000
    
    def test_same_location_distance(self):
        """Test distance between same location is zero"""
        distance = DistanceCalculator.haversine_distance(
            40.7128, -74.0060,
            40.7128, -74.0060
        )
        assert distance < 0.1  # Very close to zero
    
    def test_km_to_miles(self):
        """Test kilometer to miles conversion"""
        miles = DistanceCalculator.km_to_miles(100)
        assert 62 < miles < 63  # 100 km ≈ 62.14 miles
    
    def test_miles_to_km(self):
        """Test miles to kilometers conversion"""
        km = DistanceCalculator.miles_to_km(100)
        assert 160 < km < 161  # 100 miles ≈ 160.93 km
    
    def test_calculate_distance_between_addresses(self):
        """Test full distance calculation"""
        source_coords = {'lat': 40.7128, 'lon': -74.0060}
        dest_coords = {'lat': 34.0522, 'lon': -118.2437}
        
        result = DistanceCalculator.calculate_distance_between_addresses(
            source_coords, dest_coords
        )
        
        assert 'km' in result
        assert 'miles' in result
        assert 3900 < result['km'] < 4000
        assert 2400 < result['miles'] < 2500


class TestGeocoder:
    """Test geocoding module (requires internet)"""
    
    @pytest.mark.skipif(
        not pytest.config.getoption("--run-integration"),
        reason="Skipping integration tests (use --run-integration to run)"
    )
    def test_geocode_valid_address(self):
        """Test geocoding a valid address"""
        geocoder = Geocoder()
        coords = geocoder.geocode("Paris, France")
        
        assert 'lat' in coords
        assert 'lon' in coords
        assert 48 < coords['lat'] < 49  # Paris latitude
        assert 2 < coords['lon'] < 3    # Paris longitude
    
    @pytest.mark.skipif(
        not pytest.config.getoption("--run-integration"),
        reason="Skipping integration tests"
    )
    def test_geocode_invalid_address(self):
        """Test geocoding an invalid address"""
        geocoder = Geocoder()
        
        with pytest.raises(GeocodingError):
            geocoder.geocode("XYZ Invalid Place 123456")


def pytest_addoption(parser):
    """Add custom pytest command line option"""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests that require internet"
    )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
