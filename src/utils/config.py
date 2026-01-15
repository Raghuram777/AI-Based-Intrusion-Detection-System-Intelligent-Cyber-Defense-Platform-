"""
Configuration Module
Handles application configuration and settings
"""

import logging
import os
from typing import Dict, Any
import json

logger = logging.getLogger(__name__)


class Config:
    """
    Application configuration management.
    
    Loads settings from:
    - config.json (application settings)
    - Environment variables
    - Default values
    """
    
    # Default configuration
    DEFAULTS = {
        'network': {
            'interface': None,  # Auto-detect
            'packet_count': 1000,
            'capture_timeout': 300,
            'filter_enabled': False,
            'filter_protocol': 'TCP'
        },
        'logging': {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'file': 'logs/ids.log'
        },
        'database': {
            'type': 'sqlite',
            'path': 'data/ids.db',
            'host': 'localhost',
            'port': 3306,
            'username': 'root',
            'password': ''
        },
        'ai_models': {
            'anomaly_threshold': 0.7,
            'feature_window_size': 100,
            'model_retrain_interval': 3600,
            'learning_enabled': True
        },
        'alerts': {
            'critical_threshold': 0.9,
            'warning_threshold': 0.7,
            'enable_notifications': True
        }
    }
    
    def __init__(self, config_file: str = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to configuration file
        """
        self.config = self.DEFAULTS.copy()
        
        # Load from config file if provided
        if config_file and os.path.exists(config_file):
            self._load_from_file(config_file)
        
        # Override with environment variables
        self._load_from_env()
        
        logger.info("Configuration loaded")
    
    def _load_from_file(self, filepath: str) -> None:
        """Load configuration from JSON file"""
        try:
            with open(filepath, 'r') as f:
                file_config = json.load(f)
            
            # Deep merge with defaults
            self._deep_merge(self.config, file_config)
            logger.info(f"Configuration loaded from {filepath}")
        except Exception as e:
            logger.warning(f"Error loading config file: {e}")
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables"""
        env_mappings = {
            'NETWORK_INTERFACE': ('network', 'interface'),
            'LOG_LEVEL': ('logging', 'level'),
            'DB_TYPE': ('database', 'type'),
            'DB_PATH': ('database', 'path'),
            'ANOMALY_THRESHOLD': ('ai_models', 'anomaly_threshold'),
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                section, key = config_path
                if section in self.config:
                    self.config[section][key] = value
                    logger.debug(f"Loaded {env_var} from environment")
    
    def _deep_merge(self, base: Dict, override: Dict) -> None:
        """Recursively merge override dict into base dict"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def get(self, section: str, key: str = None, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key (optional)
            default: Default value if not found
            
        Returns:
            Configuration value
        """
        if section not in self.config:
            return default
        
        section_config = self.config[section]
        
        if key is None:
            return section_config
        
        return section_config.get(key, default)
    
    def set(self, section: str, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
        logger.debug(f"Configuration updated: {section}.{key} = {value}")
    
    def save(self, filepath: str) -> None:
        """
        Save configuration to file.
        
        Args:
            filepath: Path to save configuration file
        """
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Configuration saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self.config.copy()
