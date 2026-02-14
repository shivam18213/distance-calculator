# Distance Calculator - Modular Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT (React)                          │
│                     Frontend Application                        │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/JSON
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK APPLICATION                          │
│                         (app.py)                                │
│  ┌───────────────────────────────────────────────────────┐     │
│  │              Application Factory                      │     │
│  │  - CORS Configuration                                 │     │
│  │  - Blueprint Registration                             │     │
│  │  - Logging Setup                                      │     │
│  └───────────────────────┬───────────────────────────────┘     │
│                          │                                      │
│                          ▼                                      │
│  ┌───────────────────────────────────────────────────────┐     │
│  │              API ROUTES (routes.py)                   │     │
│  │  Blueprint: /api                                      │     │
│  │  ┌─────────────────────────────────────────────┐     │     │
│  │  │ GET  /health           - Health check       │     │     │
│  │  │ POST /calculate-distance - Calculate        │     │     │
│  │  │ GET  /history          - Get all queries    │     │     │
│  │  │ GET  /query/:id        - Get specific query │     │     │
│  │  └─────────────────────────────────────────────┘     │     │
│  └─────┬──────────┬──────────┬──────────┬────────────────┘     │
└────────┼──────────┼──────────┼──────────┼─────────────────────┘
         │          │          │          │
         ▼          ▼          ▼          ▼
┌────────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐
│ VALIDATION │ │ GEOCODING│ │  UTILS  │ │ DATABASE │
│(validation.│ │(geocoding│ │ (utils. │ │(database.│
│    py)     │ │    .py)  │ │   py)   │ │   py)    │
└────────────┘ └──────────┘ └─────────┘ └──────────┘
      │              │           │            │
      │              │           │            │
      ▼              ▼           ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────┐   ┌─────────┐
│ Security │  │Nominatim │  │Math  │   │ SQLite  │
│  Rules   │  │   API    │  │Utils │   │   DB    │
└──────────┘  └──────────┘  └──────┘   └─────────┘
```

## Module Dependencies

```
config.py
    └─> (Used by all modules for configuration)

app.py
    ├─> config.py
    └─> routes.py
            ├─> database.py
            │       └─> config.py
            ├─> geocoding.py
            │       └─> config.py
            ├─> validation.py
            │       └─> config.py
            └─> utils.py
                    └─> config.py
```

## Request Flow: Calculate Distance

```
1. Client sends POST request
   │
   ├─> /api/calculate-distance
   │   {
   │     "source": "New York, NY",
   │     "destination": "Los Angeles, CA"
   │   }
   │
   ▼
2. routes.calculate_distance() receives request
   │
   ├─> Extract JSON data
   │
   ▼
3. validation.Validator.validate_addresses()
   │
   ├─> Check length (3-200 chars)
   ├─> Detect SQL injection patterns
   └─> Trim whitespace
   │
   ▼
4. geocoding.Geocoder.geocode() (x2)
   │
   ├─> Request to Nominatim API
   ├─> Parse response
   └─> Return {lat, lon}
   │
   ▼
5. utils.DistanceCalculator.calculate_distance_between_addresses()
   │
   ├─> Apply Haversine formula
   ├─> Convert km to miles
   └─> Return distances
   │
   ▼
6. database.Database.save_query()
   │
   ├─> Open SQLite connection
   ├─> INSERT query
   └─> Return query ID
   │
   ▼
7. utils.ResponseFormatter.format_distance_response()
   │
   └─> Structure JSON response
   │
   ▼
8. Return to client
   {
     "source": "New York, NY",
     "destination": "Los Angeles, CA",
     "distance_km": 3944.42,
     "distance_miles": 2451.03,
     ...
   }
```

## Data Flow Diagram

```
┌────────────┐
│   Client   │
└──────┬─────┘
       │
       │ {source, destination}
       │
       ▼
┌────────────────┐
│  Validation    │────────┐
│  - SQL check   │        │ ValidationError
│  - Length      │        │
│  - Sanitize    │        │
└────────┬───────┘        │
         │                │
         │ Valid addresses│
         │                │
         ▼                ▼
┌────────────────┐   ┌────────┐
│   Geocoding    │   │ Error  │
│  - API call    │   │Response│
│  - Parse       │   └────────┘
└────────┬───────┘
         │
         │ {lat, lon} x2
         │
         ▼
┌────────────────┐
│  Distance      │
│  Calculation   │
│  - Haversine   │
│  - Convert     │
└────────┬───────┘
         │
         │ {km, miles}
         │
         ▼
┌────────────────┐
│   Database     │
│  - Save query  │
│  - Return ID   │
└────────┬───────┘
         │
         │ query_id
         │
         ▼
┌────────────────┐
│  Format        │
│  Response      │
└────────┬───────┘
         │
         │ JSON
         │
         ▼
┌────────────┐
│   Client   │
└────────────┘
```