# Grab the base settings
from .base import *

# Override at will!

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

##
#
##
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'stackdio',
        'HOST':     'localhost',
        'PORT':     '3306',
        'USER':     getenv('MYSQL_USER'),
        'PASSWORD': getenv('MYSQL_PASS'),
    }
}

##
# Celery & RabbitMQ
##
BROKER_URL = 'amqp://guest:guest@localhost:5672/'
