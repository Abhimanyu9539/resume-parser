import os
import sys
from loguru import logger

# Get the base directory path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define the log directory path
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Ensure the logs directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure Loguru
logger.remove()

# Define log format
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

# Add console printing
logger.add(sys.stdout, format=log_format, level="DEBUG", colorize=True)

# Add file logging (by daywise)
log_file_path = os.path.join(LOG_DIR, "{time:YYYY-MM-DD}.log")
logger.add(
    log_file_path,
    rotation="00:00",
    retention="30 days",
    format=log_format,
    level="DEBUG",
    enqueue=True,
)
