"""
Django settings for eightyseven project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from configobj import ConfigObj
from validate import Validator
from django.core.urlresolvers import reverse_lazy
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

validator = Validator()
config_path = os.path.join(BASE_DIR, "settings.ini")
config_spec = os.path.join(os.path.dirname(__file__), "settings_spec.ini")
config = ConfigObj(config_path, configspec=config_spec)
config.validate(validator)
db_dict = {
            "postgresql": "django.db.backends.postgresql_psycopg2",
            "mysql": "django.db.backends.mysql",
            "oracle": "django.db.backends.oracle",
            "sqlite": "django.db.backends.sqlite3"
            }

# general
general_config = config["general"]
ALLOWED_HOSTS = general_config["allowed_hosts"]
DEBUG = general_config["debug"]
ENABLE_REGISTRATION = general_config["enable_registration"]
LANGUAGE_CODE = general_config["language_code"]
SECRET_KEY = general_config["secret_key"]
SITE_NAME = general_config["site_name"]
TIME_ZONE = general_config["time_zone"]

# db
db_config = config["db"]
engine = db_dict[db_config["engine"]]
name = db_config["name"]
if db_config["engine"] == "sqlite":
    name = os.path.join(BASE_DIR, name)
DATABASES = {
    'default': {
        'ENGINE': engine,
        'NAME': name,
        'USER': db_config["user"],
        'PASSWORD': db_config["password"],
        'HOST': db_config["host"],
        'PORT': db_config["port"]
    }
}

# Static settings, point django at your own settings module if you need to
# override any of these or add any new options

LOGIN_URL = reverse_lazy("login")
LOGOUT_URL = reverse_lazy("logout")
LOGIN_REDIRECT_URL = reverse_lazy("home")

TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'eightyseven',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'eightyseven.urls'

WSGI_APPLICATION = 'eightyseven.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
