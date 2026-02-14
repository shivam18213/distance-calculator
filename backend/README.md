# Distance Calculator Backend - Modular Architecture

A well-structured, modular Flask backend for the Distance Calculator application.

## Architecture Overview

The backend follows a modular architecture with clear separation of concerns:

```
backend/
├── __init__.py          # Package initialization
├── app.py              # Application factory and main entry point
├── config.py           # Configuration settings
├── database.py         # Database operations and models
├── geocoding.py        # Geocoding service integration
├── routes.py           # API route definitions
├── utils.py            # Utility functions (distance calculations, formatters)
├── validation.py       # Input validation and sanitization
└── requirements.txt    # Python dependencies
```

## Module Descriptions

### `app.py` - Application Factory
- Creates and configures the Flask application
- Registers blueprints
- Sets up logging and CORS
- Main entry point for running the server

### `config.py` - Configuration Management
- Centralized configuration settings
- Environment variable support
- Constants for API endpoints, database, validation rules

### `database.py` - Database Layer
- SQLite database operations
- Context manager for connections
- CRUD operations for query history
- Automatic database initialization

### `geocoding.py` - Geocoding Service
- Nominatim API integration
- Address to coordinates conversion
- Reverse geocoding support
- Batch geocoding capabilities
- Custom exception handling

### `routes.py` - API Routes
- RESTful endpoint definitions
- Request/response handling
- Coordinates all services (validation, geocoding, database)
- Error handling and logging

### `validation.py` - Input Validation
- Address validation with security checks
- SQL injection prevention
- Input sanitization
- Coordinate validation
- Custom validation exceptions

### `utils.py` - Utilities
- Haversine distance calculation
- Unit conversions (km ↔ miles)
- Response formatting
- Helper functions

## Getting Started

### Installation

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Run with default settings
python app.py

# Or with custom environment variables
export FLASK_DEBUG=False
export FLASK_PORT=8000
python app.py
```

The server will start on `http://localhost:5000` by default.

## Configuration

Configure the application using environment variables:

```bash
# Flask settings
export FLASK_DEBUG=True          # Enable debug mode
export FLASK_HOST=0.0.0.0        # Host to bind to
export FLASK_PORT=5000           # Port to listen on

# Database
export DATABASE_NAME=queries.db  # Database file name

# Logging
export LOG_LEVEL=INFO            # Logging level (DEBUG, INFO, WARNING, ERROR)
```

Or modify `config.py` directly for permanent changes.

## 📡 API Endpoints

### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

### Calculate Distance
```http
POST /api/calculate-distance
Content-Type: application/json

{
  "source": "New York, NY",
  "destination": "Los Angeles, CA"
}
```

**Response:**
```json
{
  "source": "New York, NY",
  "destination": "Los Angeles, CA",
  "distance_km": 3944.42,
  "distance_miles": 2451.03,
  "source_coords": {"lat": 40.7128, "lon": -74.0060},
  "destination_coords": {"lat": 34.0522, "lon": -118.2437}
}
```

### Get History
```http
GET /api/history?limit=50
```

**Response:**
```json
{
  "queries": [
    {
      "id": 1,
      "source": "New York, NY",
      "destination": "Los Angeles, CA",
      "distance_km": 3944.42,
      "distance_miles": 2451.03,
      "source_coords": {"lat": 40.7128, "lon": -74.0060},
      "destination_coords": {"lat": 34.0522, "lon": -118.2437},
      "timestamp": "2024-02-10 14:30:00"
    }
  ],
  "count": 1
}
```

### Get Specific Query
```http
GET /api/query/1
```

**Response:**
```json
{
  "id": 1,
  "source": "New York, NY",
  "destination": "Los Angeles, CA",
  "distance_km": 3944.42,
  "distance_miles": 2451.03,
  "source_coords": {"lat": 40.7128, "lon": -74.0060},
  "destination_coords": {"lat": 34.0522, "lon": -118.2437},
  "timestamp": "2024-02-10 14:30:00"
}
```

## 🔒 Security Features

### Input Validation
- **Address Length**: 3-200 characters
- **SQL Injection Prevention**: Pattern matching for malicious SQL
- **Type Checking**: Strict type validation
- **Sanitization**: Whitespace trimming, null byte detection

### Error Handling
- Graceful degradation
- Comprehensive logging
- User-friendly error messages
- No sensitive data exposure

### Database Security
- Parameterized queries (prevents SQL injection)
- Connection context managers
- Transaction rollback on errors

## 🧪 Testing

### Manual Testing

```bash
# Test with curl
curl -X POST http://localhost:5000/api/calculate-distance \
  -H "Content-Type: application/json" \
  -d '{"source": "Paris, France", "destination": "London, UK"}'

# Get history
curl http://localhost:5000/api/history?limit=10

# Health check
curl http://localhost:5000/api/health
```


## Database Schema

```sql
CREATE TABLE queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_address TEXT NOT NULL,
    destination_address TEXT NOT NULL,
    source_lat REAL NOT NULL,
    source_lon REAL NOT NULL,
    dest_lat REAL NOT NULL,
    dest_lon REAL NOT NULL,
    distance_km REAL NOT NULL,
    distance_miles REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```


## Troubleshooting

**Import errors**:
```bash
# Make sure you're in the correct directory
cd backend
python app.py
```

**Database locked**:
```bash
# Close any other connections to the database
# Or delete the .db file to start fresh
rm distance_queries.db
```

**Geocoding failures**:
- Check internet connection
- Verify Nominatim API is accessible
- Respect rate limits (1 request/second)

## Code Quality

The modular architecture provides:

**Separation of Concerns**: Each module has a single responsibility
**Testability**: Easy to unit test individual modules
**Maintainability**: Clear structure makes updates simple
**Scalability**: Easy to add new features
**Reusability**: Modules can be imported independently
**Type Hints**: Better IDE support and documentation
**Error Handling**: Comprehensive exception handling
**Logging**: Detailed logging throughout