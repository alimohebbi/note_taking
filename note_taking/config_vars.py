import os
from pathlib import Path

SECRET_KEY = 'django-insecure-i900b-3!gs6gy2s0b)c3c8x@5t2a(7gryv72v1dd%)wrt&!6s4'
BASE_DIR = Path(__file__).resolve().parent.parent

database_info = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'note-db',
        'USER': 'note-admin',
        'PASSWORD': 'dENgczA44IsDn',
        'HOST': 'localhost',  # Set to the host where your PostgreSQL server is running.
        'PORT': '',  # Leave it as an empty string for the default PostgreSQL port (5432).
    }
}

OBJECTS_BATCH_SIZE = 17

logging_conf = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/info.log'),  # Adjust the path as needed
            'maxBytes': 1024 * 1024,  # 1 MB
            'backupCount': 10,  # Keep up to 10 log files
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
}
