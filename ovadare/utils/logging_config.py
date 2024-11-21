# ovadare/utils/logging_config.py

"""
Logging Configuration Module for the Ovadare Framework

This module configures logging settings for the framework, including log
formats, levels, handlers, and integration with the Configuration module.
"""

import logging
import logging.config
from ovadare.utils.configuration import Configuration

def setup_logging() -> None:
    """
    Sets up logging configuration based on settings from the Configuration module.
    """
    logging_level = Configuration.get('logging_level', 'INFO').upper()
    log_format = Configuration.get('log_format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_datefmt = Configuration.get('log_datefmt', '%Y-%m-%d %H:%M:%S')
    log_file = Configuration.get('log_file', None)

    handlers = ['console']
    if log_file:
        handlers.append('file')

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': log_format,
                'datefmt': log_datefmt
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': logging_level,
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'level': logging_level,
                'filename': log_file
            }
        },
        'root': {
            'handlers': handlers,
            'level': logging_level
        },
    }

    logging.config.dictConfig(logging_config)
    logging.getLogger().info("Logging configuration has been set up.")


# Initialize logging when the module is imported
setup_logging()
