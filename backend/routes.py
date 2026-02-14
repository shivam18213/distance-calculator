from flask import Blueprint, request, jsonify
import logging

from database import Database
from geocoding import Geocoder, GeocodingError
from validation import Validator, ValidationError
from utils import DistanceCalculator, ResponseFormatter

logger = logging.getLogger(__name__)

# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api')

# Initialize services
db = Database()
geocoder = Geocoder()


@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


@api.route('/calculate-distance', methods=['POST'])
def calculate_distance():
    """
    Calculate distance between two addresses
    
    Request Body:
        {
            "source": "Address 1",
            "destination": "Address 2"
        }
    
    Response:
        {
            "source": "Address 1",
            "destination": "Address 2",
            "distance_km": 100.5,
            "distance_miles": 62.4,
            "source_coords": {"lat": 40.7, "lon": -74.0},
            "destination_coords": {"lat": 34.0, "lon": -118.2}
        }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            logger.warning("No data provided in request")
            return ResponseFormatter.format_error_response('No data provided', 400)
        
        source = data.get('source', '').strip()
        destination = data.get('destination', '').strip()
        
        # Validate inputs
        try:
            source, destination = Validator.validate_addresses(source, destination)
        except ValidationError as e:
            logger.warning(f"Validation error: {str(e)}")
            return ResponseFormatter.format_error_response(str(e), 400)
        
        # Geocode addresses
        try:
            source_coords = geocoder.geocode(source)
        except GeocodingError as e:
            logger.error(f"Failed to geocode source: {str(e)}")
            return ResponseFormatter.format_error_response(str(e), 404)
        
        try:
            dest_coords = geocoder.geocode(destination)
        except GeocodingError as e:
            logger.error(f"Failed to geocode destination: {str(e)}")
            return ResponseFormatter.format_error_response(str(e), 404)
        
        # Calculate distance
        distance = DistanceCalculator.calculate_distance_between_addresses(
            source_coords, dest_coords
        )
        
        logger.info(f"Calculated distance: {distance['km']:.2f} km / {distance['miles']:.2f} miles")
        
        # Save to database
        try:
            query_id = db.save_query(
                source, destination,
                source_coords['lat'], source_coords['lon'],
                dest_coords['lat'], dest_coords['lon'],
                distance['km'], distance['miles']
            )
            logger.info(f"Query saved with ID: {query_id}")
        except Exception as e:
            logger.error(f"Failed to save query: {str(e)}")
            # Continue even if saving fails
        
        # Format and return response
        response = ResponseFormatter.format_distance_response(
            source, destination,
            source_coords, dest_coords,
            distance['km'], distance['miles']
        )
        
        return ResponseFormatter.format_success_response(response, 200)
        
    except Exception as e:
        logger.error(f"Unexpected error in calculate_distance: {str(e)}")
        return ResponseFormatter.format_error_response(
            'An unexpected error occurred. Please try again.', 500
        )


@api.route('/history', methods=['GET'])
def get_history():
    """
    Retrieve past distance queries
    
    Query Parameters:
        limit (int, optional): Maximum number of records to return (default: 50, max: 100)
    
    Response:
        {
            "queries": [
                {
                    "id": 1,
                    "source": "Address 1",
                    "destination": "Address 2",
                    "distance_km": 100.5,
                    "distance_miles": 62.4,
                    "source_coords": {"lat": 40.7, "lon": -74.0},
                    "destination_coords": {"lat": 34.0, "lon": -118.2},
                    "timestamp": "2024-02-10 14:30:00"
                }
            ],
            "count": 1
        }
    """
    try:
        # Get and validate limit parameter
        limit = request.args.get('limit', 50, type=int)
        limit = Validator.validate_limit(limit)
        
        logger.info(f"Fetching query history (limit: {limit})")
        
        # Retrieve history from database
        queries = db.get_history(limit)
        
        # Format and return response
        response = ResponseFormatter.format_history_response(queries)
        return ResponseFormatter.format_success_response(response, 200)
        
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        return ResponseFormatter.format_error_response(
            'Failed to retrieve history', 500
        )


@api.route('/query/<int:query_id>', methods=['GET'])
def get_query(query_id):
    """
    Retrieve a specific query by ID
    
    Path Parameters:
        query_id (int): ID of the query
    
    Response:
        {
            "id": 1,
            "source": "Address 1",
            "destination": "Address 2",
            "distance_km": 100.5,
            "distance_miles": 62.4,
            "source_coords": {"lat": 40.7, "lon": -74.0},
            "destination_coords": {"lat": 34.0, "lon": -118.2},
            "timestamp": "2024-02-10 14:30:00"
        }
    """
    try:
        query = db.get_query_by_id(query_id)
        
        if not query:
            return ResponseFormatter.format_error_response(
                f'Query with ID {query_id} not found', 404
            )
        
        return ResponseFormatter.format_success_response(query, 200)
        
    except Exception as e:
        logger.error(f"Error retrieving query {query_id}: {str(e)}")
        return ResponseFormatter.format_error_response(
            'Failed to retrieve query', 500
        )
