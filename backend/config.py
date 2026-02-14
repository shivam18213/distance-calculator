class Config:
    # app configs
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000

    
    # distance queris db
    DATABASE_NAME = 'distance_queries.db'

    # nomination db
    NOMINATIM_BASE_URL = 'https://nominatim.openstreetmap.org'
    NOMINATIM_TIMEOUT = 10
    NOMINATIM_USER_AGENT = 'DistanceCalculatorApp/1.0'
    
    # limit configs
    MAX_HISTORY_LIMIT = 100
    DEFAULT_HISTORY_LIMIT = 50
    MIN_ADDRESS_LENGTH = 3
    MAX_ADDRESS_LENGTH = 200
    EARTH_RADIUS_KM = 6371
    KM_TO_MILES_FACTOR = 0.621371
    
    # logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
