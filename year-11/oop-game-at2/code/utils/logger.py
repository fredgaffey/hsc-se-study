"""
Logger module.

This module provides a centralized logging system for the game.
"""

import os
import logging
import sys
from logging.handlers import RotatingFileHandler

# Define log directory
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")

# Create logs directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Log file path
LOG_FILE_PATH = os.path.join(LOG_DIR, "game.log")

# Configure logging levels
LOG_LEVEL_FILE = logging.DEBUG
LOG_LEVEL_CONSOLE = logging.INFO

# Configure logging format
LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_logger(name):
    """
    Get a configured logger instance.
    
    Args:
        name (str): The name of the logger.
        
    Returns:
        logging.Logger: A configured logger instance.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Only add handlers if none exist
    if not logger.handlers:
        # File handler (rotates log files)
        file_handler = RotatingFileHandler(
            LOG_FILE_PATH, maxBytes=1024*1024*5, backupCount=5
        )
        file_handler.setLevel(LOG_LEVEL_FILE)
        file_handler.setFormatter(LOG_FORMAT)
        logger.addHandler(file_handler)
        
        # Console handler (only shows INFO and above)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(LOG_LEVEL_CONSOLE)
        console_handler.setFormatter(LOG_FORMAT)
        logger.addHandler(console_handler)
    
    return logger

# Main logger for the game
game_logger = get_logger("game")

# Asset loader logger
asset_logger = get_logger("asset_loader")

# Map loader logger
map_logger = get_logger("map_loader")

# Character logger
character_logger = get_logger("character")

# Utility functions to simplify logging calls
def debug(msg, logger=game_logger):
    """Log a debug message."""
    logger.debug(msg)

def info(msg, logger=game_logger):
    """Log an info message."""
    logger.info(msg)

def warning(msg, logger=game_logger):
    """Log a warning message."""
    logger.warning(msg)

def error(msg, logger=game_logger):
    """Log an error message."""
    logger.error(msg)

def critical(msg, logger=game_logger):
    """Log a critical message."""
    logger.critical(msg)

def exception(msg, logger=game_logger):
    """Log an exception message with traceback."""
    logger.exception(msg)