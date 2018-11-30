from config.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wgb',
        'USER': 'tevasaki',
        'PASSWORD': 'teVa0210',
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
          'autocommit': False,
        },
        'HOST': '192.168.20.42',
    }
}