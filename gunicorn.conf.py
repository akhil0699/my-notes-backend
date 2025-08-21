# Gunicorn configuration file
import multiprocessing

max_requests = 1000  # pylint: disable=C0103
max_requests_jitter = 50  # pylint: disable=C0103

reload = False

capture_output = True
bind = "0.0.0.0:10000"  # pylint: disable=C0103

worker_class = "uvicorn.workers.UvicornWorker"  # pylint: disable=C0103
workers = 1

# Gunicorn logging configuration
accesslog = "-"
errorlog = "-"  # logs to stdout
loglevel = "info"
access_log_format = "%(t)s [%(p)s] [%(l)s] [%(m)s :: %(U)s :: %(q)s]"

# Disable Uvicorn logs
logger_class = "gunicorn.glogging.Logger"
logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
        },
        "gunicorn_handler": {
            "class": "logging.StreamHandler",
            "formatter": "gunicorn_request",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "gunicorn": {"propogate": True},
        "gunicorn.access": {"propogate": True, "handlers": ["gunicorn_handler"], "level": "INFO"},
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "formatters": {
        "gunicorn_request": {
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}
