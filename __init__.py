"""
Distance Calculator Backend API
A modular Flask application for calculating distances between addresses
"""

__version__ = '1.0.0'
__author__ = 'Distance Calculator Team'

from .app import create_app

__all__ = ['create_app']
