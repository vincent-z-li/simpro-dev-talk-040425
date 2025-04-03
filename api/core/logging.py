import logging
from logging.config import dictConfig

def setup_logging():
    """Configure logging for the application."""
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "loggers": {
            "app": {"handlers": ["console"], "level": "INFO", "propagate": True},
        },
    }
    dictConfig(logging_config)
    return logging.getLogger("app")

logger = setup_logging()
