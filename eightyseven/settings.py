##
#    Copyright (C) 2014 Jessica Tallon & Matt Molyneaux
#
#    This file is part of Inboxen.
#
#    Inboxen is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Inboxen is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Inboxen  If not, see <http://www.gnu.org/licenses/>.
##

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

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)

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

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
