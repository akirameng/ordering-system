"""
Django settings for OrderingSystem project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'iamoxx3s(1v&ubkhw_=y#r9kiz+(=!x(e5enw#ou#hr&+m4l-9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'registration',
    'accounts',
    'business',
    'Customer',
    'rest_framework',
    'social.apps.django_app.default',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

ROOT_URLCONF = 'OrderingSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'accounts.pipeline.save_profile_picture',
    )

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

WSGI_APPLICATION = 'OrderingSystem.wsgi.application'
SITE_ID = 1
AUTH_PROFILE_MODULE = 'accounts.CustomUser'
AUTH_USER_MODEL = 'accounts.CustomUser'


LOGIN_REDIRECT_URL = '/accounts/success/'  # The page you want users to arrive at after they successful log in
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_ERROR = 'accounts/error/'

SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/accounts/'
import random
SOCIAL_AUTH_DEFAULT_USERNAME = lambda: random.choice(['Darth Vader', 'Obi-Wan Kenobi', 'R2-D2', 'C-3PO', 'Yoda'])

# test localhost client ID for google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '446972796364-19cou22lhvu7fut5pd895rgk5hij5meu.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'u_NlWE3Q4kShm6P5-uUkDYTq'

# server client ID for google
#SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '446972796364-nkt057t5qb1d5makn1g0f39jfj5vk544.apps.googleusercontent.com'
#SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'FboX7ImKltn0RAFeOPZrDOvT'

# test facebook server test app credentials
#SOCIAL_AUTH_FACEBOOK_KEY = '410211035848139'
#SOCIAL_AUTH_FACEBOOK_SECRET = 'e12c72b3b61caadc1be857e11d01d276'

# test facebook localhost test app credentials
SOCIAL_AUTH_FACEBOOK_KEY = '410208442515065'
SOCIAL_AUTH_FACEBOOK_SECRET = '45c8ee2aeb57bdb35de0d9d6617ef399'

# facebook app credentials
# SOCIAL_AUTH_FACEBOOK_KEY = '410206499181926'
# SOCIAL_AUTH_FACEBOOK_SECRET = '70f7974d82548ac03a88a1aa53b62ee8'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email',]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ordering.system.no.reply'
EMAIL_HOST_PASSWORD = 'Aa1013527'
EMAIL_PORT = 587
SERVER_EMAIL = 'ordering.system.no.reply@gmail.com'
DEFAULT_FROM_EMAIL = 'ordering.system.no.reply@gmail.com'

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
REGISTRATION_EMAIL_HTML = True

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Vancouver'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = (os.path.join(BASE_DIR, "media"))

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    (os.path.join(BASE_DIR, "static")),
)

