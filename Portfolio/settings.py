"""
Django settings for Portfolio project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from etc import keys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = keys.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["https://hinacio.com", "https://www.hinacio.com", "hinacio.com", "www.hinacio.com", "https://portfolio-g0ri.onrender.com/", "https://www.portfolio-g0ri.onrender.com/"]

CSRF_TRUSTED_ORIGINS = ["https://hinacio.com", "https://www.hinacio.com", "hinacio.com", "www.hinacio.com", "https://portfolio-g0ri.onrender.com/", "https://www.portfolio-g0ri.onrender.com/"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Main.apps.MainConfig',
    'login.apps.LoginConfig',
    'messageapp.apps.MessageappConfig',
    'TDV.apps.TdvConfig',
    'TG2A.apps.Tg2AConfig',
    'crispy_forms',
    'social_django',
    'django_apscheduler',
    'cloudinary_storage',
    'cloudinary',

]

CLOUDINARY_STORAGE = {
             'CLOUD_NAME': 'htmz79u9f',
             'API_KEY': '569142699516489',
             'API_SECRET': keys.CLOUDINARY_API_KEY
            }


SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'Portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]




WSGI_APPLICATION = 'Portfolio.wsgi.application'

ASGI_APPLICATION = "Portfolio.asgi.application"


# Channels
ASGI_APPLICATION = 'Portfolio.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'port_db',
        'USER': 'port_db_user',
        'PASSWORD': keys.DATABASE_PASS,
        'HOST': 'dpg-ch8edao2qv2864slta90-a',
        'PORT': 5432,
        }

}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 6,
            }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',


    'django.contrib.auth.backends.ModelBackend',
)


SOCIAL_AUTH_GITHUB_KEY = '66635515d763aef57209'
SOCIAL_AUTH_GITHUB_SECRET = keys.GIT_KEY

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '945179667763-h7m4q8oee5qaeqpordsagt6bjgd8nmbe.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = keys.GOOGLE_KEY

ENCRYPT_KEY = keys.ENCRYPT_KEY




# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SENDGRID_API_KEY = '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'
DEFAULT_FROM_EMAIL = 'me@hinacio.com'
SERVER_EMAIL = 'hinaciosant@gmail.com'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = keys.EMAIL_PASS
EMAIL_USE_TLS = True

# Static files (CSS, Javgcript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_FILE_STORAGE='cloudinary_storage.storage.MediaCloudinaryStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]


CRISPY_TEMPLATE_PACK="bootstrap4"

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
