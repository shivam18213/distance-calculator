"""
Main application module
Flask application factory and initialization
"""

from flask import Flask
from flask_cors import CORS
import logging

from config import Config
from routes import api


def create_app(config=None):
    """
    Application factory for creating Flask app
    
    Args:
        config: Optional configuration object
        
    Returns:
        Configured Flask application
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    if config:
        app.config.from_object(config)
    else:
        app.config.from_object(Config)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format=Config.LOG_FORMAT
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Initializing Distance Calculator API")
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api)
    
    logger.info("Application initialized successfully")
    
    return app


def main():
    """Main entry point for running the application"""
    app = create_app()
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting server on {Config.HOST}:{Config.PORT}")
    
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )


if __name__ == '__main__':
    main()
