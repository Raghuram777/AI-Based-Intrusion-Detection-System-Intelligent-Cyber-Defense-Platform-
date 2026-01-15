"""
AI-Powered Intrusion Detection System (AI-IDS)
Main source package initialization
"""

__version__ = "0.1.0"
__author__ = "AI-IDS Development Team"
__description__ = "Enterprise-grade AI-powered Intrusion Detection System"

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info(f"AI-IDS v{__version__} initialized")
