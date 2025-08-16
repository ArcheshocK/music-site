# from datetime import timedelta
from pathlib import Path

# flaw 6: Identification and Authentication Failures (A07:2021)
# Djangos default login view does not provide any rate limiting or lockout mechanism
# so without additional protection, the app is vulnerable to brute force login attempts

# suggested fix :
# you can use a package like django-axes:
# INSTALLED_APPS += ['axes']
# MIDDLEWARE.insert(0, 'axes.middleware.AxesMiddleware')
# AXES_FAILURE_LIMIT = 5
# AXES_COOLOFF_TIME = timedelta(minutes=30)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8o0u8_e!replace-this-in-prod!9y)w&2f8'

# flaw 2: Sensitive Data Exposure (A04:2021)
#  secret key is hardcoded and visible. In a real deployment, this should be set as an environment variable.

# flaw 5: Security Misconfiguration (A05:2021)
DEBUG = True
# Debug mode is left on which can expose sensitive information if deployed in production
# suggested fix:
# DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'music_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'music_site.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'music_list'
LOGOUT_REDIRECT_URL = 'login'
MUSIC_ROOT = BASE_DIR / 'music_files'
ALLOWED_EXTENSIONS = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'}
