import logging
import os
from datetime import datetime

class BotLogger:
    def __init__(self):
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger('RedditBot')
        self.logger.setLevel(logging.INFO)
        
        # File handler
        log_filename = f"logs/reddit_bot_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
    
    def log(self, message, level='info'):
        """Log a message"""
        if level == 'info':
            self.logger.info(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'warning':
            self.logger.warning(message)