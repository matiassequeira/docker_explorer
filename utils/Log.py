import logging
import logging.config
import traceback
import os

logger=None
level= logging.DEBUG
os.makedirs("logs", exist_ok=True)
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "class": "logging.Formatter",
                "style": "{",
                "datefmt": "%Y-%m-%d %H:%M",
                "format": "[{asctime:s}] {message:s}"
            }
        },
        "handlers": {
            "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": level
            },
            "file": {
                "level": level,
                "class": "logging.handlers.WatchedFileHandler",
                "formatter": "default",
                "filename": "logs/docker_explorer.log",
                "mode": "a",
                "encoding": "utf-8"
            }
        },
        'root': {'handlers': ('console', 'file')}
    }
)

def getLogger(name):
    global logger
    if logger is None:
        logger = logging.getLogger(name)
        logger.setLevel(level)
    return logger