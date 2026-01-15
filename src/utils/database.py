"""
Database Module
Handles storage of alerts, events, and statistics
"""

import logging
import sqlite3
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)


class Database:
    """
    Database management for AI-IDS.
    
    Supports:
    - SQLite for local storage
    - Alert storage
    - Event logging
    - Model statistics tracking
    """
    
    def __init__(self, db_path: str = 'data/ids.db'):
        """
        Initialize database.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        
        # Create directory if needed
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self._initialize_database()
        logger.info(f"Database initialized at {db_path}")
    
    def _initialize_database(self) -> None:
        """Create database tables if they don't exist"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            cursor = self.connection.cursor()
            
            # Alerts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    alert_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    source_ip TEXT,
                    destination_ip TEXT,
                    protocol TEXT,
                    description TEXT,
                    indicators TEXT,
                    recommendation TEXT,
                    acknowledged INTEGER DEFAULT 0,
                    false_positive INTEGER DEFAULT 0
                )
            ''')
            
            # Events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    event_type TEXT NOT NULL,
                    source TEXT,
                    message TEXT,
                    severity TEXT,
                    indicators TEXT
                )
            ''')
            
            # Statistics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metric_name TEXT NOT NULL,
                    metric_value REAL,
                    additional_data TEXT
                )
            ''')
            
            # Model performance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS model_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    model_name TEXT NOT NULL,
                    accuracy REAL,
                    precision REAL,
                    recall REAL,
                    f1_score REAL,
                    test_samples INTEGER
                )
            ''')
            
            self.connection.commit()
            logger.info("Database tables created successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def insert_alert(self, alert_data: Dict) -> int:
        """
        Insert an alert into the database.
        
        Args:
            alert_data: Dictionary with alert information
            
        Returns:
            Alert ID
        """
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT INTO alerts (
                    alert_type, severity, confidence, source_ip,
                    destination_ip, protocol, description, indicators, recommendation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert_data.get('alert_type'),
                alert_data.get('severity'),
                alert_data.get('confidence', 0),
                alert_data.get('source_ip'),
                alert_data.get('destination_ip'),
                alert_data.get('protocol'),
                alert_data.get('description'),
                json.dumps(alert_data.get('indicators', [])),
                alert_data.get('recommendation')
            ))
            
            self.connection.commit()
            alert_id = cursor.lastrowid
            logger.debug(f"Alert inserted with ID {alert_id}")
            return alert_id
            
        except Exception as e:
            logger.error(f"Error inserting alert: {e}")
            return -1
    
    def insert_event(self, event_data: Dict) -> int:
        """
        Insert an event into the database.
        
        Args:
            event_data: Dictionary with event information
            
        Returns:
            Event ID
        """
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT INTO events (
                    event_type, source, message, severity, indicators
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                event_data.get('event_type'),
                event_data.get('source'),
                event_data.get('message'),
                event_data.get('severity'),
                json.dumps(event_data.get('indicators', []))
            ))
            
            self.connection.commit()
            event_id = cursor.lastrowid
            logger.debug(f"Event inserted with ID {event_id}")
            return event_id
            
        except Exception as e:
            logger.error(f"Error inserting event: {e}")
            return -1
    
    def get_alerts(self, limit: int = 100, severity: str = None) -> List[Dict]:
        """
        Get alerts from database.
        
        Args:
            limit: Maximum number of alerts to retrieve
            severity: Filter by severity level
            
        Returns:
            List of alert dictionaries
        """
        try:
            cursor = self.connection.cursor()
            
            if severity:
                cursor.execute('''
                    SELECT * FROM alerts
                    WHERE severity = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (severity, limit))
            else:
                cursor.execute('''
                    SELECT * FROM alerts
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
            
            columns = [desc[0] for desc in cursor.description]
            alerts = []
            
            for row in cursor.fetchall():
                alert = dict(zip(columns, row))
                if alert.get('indicators'):
                    alert['indicators'] = json.loads(alert['indicators'])
                alerts.append(alert)
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error retrieving alerts: {e}")
            return []
    
    def get_events(self, limit: int = 100, hours: int = 24) -> List[Dict]:
        """
        Get recent events from database.
        
        Args:
            limit: Maximum number of events
            hours: Time window in hours
            
        Returns:
            List of event dictionaries
        """
        try:
            cursor = self.connection.cursor()
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            cursor.execute('''
                SELECT * FROM events
                WHERE timestamp > ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (cutoff_time.isoformat(), limit))
            
            columns = [desc[0] for desc in cursor.description]
            events = []
            
            for row in cursor.fetchall():
                event = dict(zip(columns, row))
                if event.get('indicators'):
                    event['indicators'] = json.loads(event['indicators'])
                events.append(event)
            
            return events
            
        except Exception as e:
            logger.error(f"Error retrieving events: {e}")
            return []
    
    def get_alert_statistics(self, hours: int = 24) -> Dict:
        """
        Get alert statistics.
        
        Args:
            hours: Time window in hours
            
        Returns:
            Dictionary with alert statistics
        """
        try:
            cursor = self.connection.cursor()
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Total alerts
            cursor.execute('''
                SELECT COUNT(*) FROM alerts WHERE timestamp > ?
            ''', (cutoff_time.isoformat(),))
            total_alerts = cursor.fetchone()[0]
            
            # Alerts by severity
            cursor.execute('''
                SELECT severity, COUNT(*) FROM alerts
                WHERE timestamp > ?
                GROUP BY severity
            ''', (cutoff_time.isoformat(),))
            severity_counts = dict(cursor.fetchall())
            
            # Average confidence
            cursor.execute('''
                SELECT AVG(confidence) FROM alerts
                WHERE timestamp > ?
            ''', (cutoff_time.isoformat(),))
            avg_confidence = cursor.fetchone()[0] or 0
            
            return {
                'total_alerts': total_alerts,
                'severity_distribution': severity_counts,
                'average_confidence': round(avg_confidence, 3),
                'time_window_hours': hours
            }
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
    
    def insert_statistic(self, metric_name: str, metric_value: float, 
                        additional_data: Dict = None) -> int:
        """
        Insert a statistic into the database.
        
        Args:
            metric_name: Name of the metric
            metric_value: Metric value
            additional_data: Additional data dictionary
            
        Returns:
            Statistic ID
        """
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT INTO statistics (
                    metric_name, metric_value, additional_data
                ) VALUES (?, ?, ?)
            ''', (
                metric_name,
                metric_value,
                json.dumps(additional_data) if additional_data else None
            ))
            
            self.connection.commit()
            return cursor.lastrowid
            
        except Exception as e:
            logger.error(f"Error inserting statistic: {e}")
            return -1
    
    def mark_alert_as_acknowledged(self, alert_id: int) -> bool:
        """Mark an alert as acknowledged"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE alerts SET acknowledged = 1 WHERE id = ?
            ''', (alert_id,))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating alert: {e}")
            return False
    
    def mark_alert_as_false_positive(self, alert_id: int) -> bool:
        """Mark an alert as false positive for model retraining"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE alerts SET false_positive = 1 WHERE id = ?
            ''', (alert_id,))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating alert: {e}")
            return False
    
    def close(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def __del__(self):
        """Ensure database connection is closed"""
        self.close()
