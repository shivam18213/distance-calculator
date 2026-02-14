import sqlite3
import logging
from typing import List, Dict, Optional
from contextlib import contextmanager

from config import Config

logger = logging.getLogger(__name__)


class Database:
    #Database handler for distance queries
    
    def __init__(self, db_name: str = ""):
        self.db_name = db_name or Config.DATABASE_NAME
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def init_db(self):
        """Initialize database with required tables"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS queries (
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
                    )
                ''')
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise
    
    def save_query(
        self,
        source_address: str,
        destination_address: str,
        source_lat: float,
        source_lon: float,
        dest_lat: float,
        dest_lon: float,
        distance_km: float,
        distance_miles: float
    ) -> int:
        """
        Save a distance query to the database
        
        Returns:
            int: ID of the inserted record
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO queries 
                    (source_address, destination_address, source_lat, source_lon, 
                     dest_lat, dest_lon, distance_km, distance_miles)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    source_address, destination_address,
                    source_lat, source_lon,
                    dest_lat, dest_lon,
                    distance_km, distance_miles
                ))
                query_id = cursor.lastrowid or 0
                logger.info(f"Query saved to database with ID: {query_id}")
                return query_id
        except Exception as e:
            logger.error(f"Failed to save query: {str(e)}")
            raise
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Retrieve query history from database
        
        Args:
            limit: Maximum number of records to retrieve
            
        Returns:
            List of query dictionaries
        """
        limit = limit or Config.DEFAULT_HISTORY_LIMIT
        limit = min(limit, Config.MAX_HISTORY_LIMIT)
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        id,
                        source_address,
                        destination_address,
                        source_lat,
                        source_lon,
                        dest_lat,
                        dest_lon,
                        distance_km,
                        distance_miles,
                        timestamp
                    FROM queries
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
                
                rows = cursor.fetchall()
                
                # Convert to list of dictionaries
                history = []
                for row in rows:
                    history.append({
                        'id': row['id'],
                        'source': row['source_address'],
                        'destination': row['destination_address'],
                        'source_coords': {
                            'lat': row['source_lat'],
                            'lon': row['source_lon']
                        },
                        'destination_coords': {
                            'lat': row['dest_lat'],
                            'lon': row['dest_lon']
                        },
                        'distance_km': round(row['distance_km'], 2),
                        'distance_miles': round(row['distance_miles'], 2),
                        'timestamp': row['timestamp']
                    })
                
                logger.info(f"Retrieved {len(history)} historical queries")
                return history
                
        except Exception as e:
            logger.error(f"Failed to retrieve history: {str(e)}")
            raise
    
    def get_query_by_id(self, query_id: int) -> Optional[Dict]:
        """
        Retrieve a specific query by ID
        
        Args:
            query_id: ID of the query to retrieve
            
        Returns:
            Query dictionary or None if not found
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM queries WHERE id = ?
                ''', (query_id,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                return {
                    'id': row['id'],
                    'source': row['source_address'],
                    'destination': row['destination_address'],
                    'source_coords': {
                        'lat': row['source_lat'],
                        'lon': row['source_lon']
                    },
                    'destination_coords': {
                        'lat': row['dest_lat'],
                        'lon': row['dest_lon']
                    },
                    'distance_km': round(row['distance_km'], 2),
                    'distance_miles': round(row['distance_miles'], 2),
                    'timestamp': row['timestamp']
                }
        except Exception as e:
            logger.error(f"Failed to retrieve query {query_id}: {str(e)}")
            raise
    
    def clear_history(self):
        """Clear all query history (use with caution)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM queries')
                deleted_count = cursor.rowcount
                logger.warning(f"Cleared {deleted_count} queries from history")
                return deleted_count
        except Exception as e:
            logger.error(f"Failed to clear history: {str(e)}")
            raise
