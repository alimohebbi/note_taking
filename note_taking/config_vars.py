SECRET_KEY = 'django-insecure-i900b-3!gs6gy2s0b)c3c8x@5t2a(7gryv72v1dd%)wrt&!6s4'

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
