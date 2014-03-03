# Grab the base settings
from .base import *  # NOQA

# Override at will!

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

##
# Celery & RabbitMQ
##
BROKER_URL = 'amqp://guest:guest@localhost:5672/'

##
# Add in additional middleware
##
MIDDLEWARE_CLASSES += (
    'core.middleware.JSONIndentAcceptHeaderMiddleware',
)

##
# Add in additional applications
##
#INSTALLED_APPS += ('',)
