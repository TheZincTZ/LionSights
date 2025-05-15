import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging():
    """Configure logging for the application"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Generate log filename with date
    log_filename = f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.handlers.RotatingFileHandler(
                log_filename,
                maxBytes=10485760,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )

    # Set specific log levels for different modules
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)
    logging.getLogger('streamlit').setLevel(logging.WARNING)

    return logging.getLogger(__name__) 