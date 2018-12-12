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
        # 'HOST': '192.168.20.42',
    }
}

MEDIA_URL = '/upload/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')

