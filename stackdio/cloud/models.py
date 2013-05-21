import logging

from django.conf import settings
from django.db import models
from django.core.files.storage import FileSystemStorage

from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel

from core.fields import DeletingFileField

logger = logging.getLogger(__name__)

def get_private_key_file_path(obj, filename):
    '''
    Determines the path to where private key files are stored.
    '''

    return "cloud/{0}/keys/{1}".format(obj.slug, filename)

class CloudProviderType(models.Model):


    # TODO: Probably should detect what providers are available, but how?
    PROVIDER_TYPES = (('aws', 'AWS'),)

    type_name = models.CharField(max_length=32, choices=PROVIDER_TYPES, unique=True)

    def __unicode__(self):
        return self.type_name

class CloudProvider(TimeStampedModel, TitleSlugDescriptionModel):


    # What is the type of provider (e.g., AWS, Rackspace, etc)
    provider_type = models.ForeignKey('CloudProviderType')

    # Used to store the provider-specifc YAML that will be written
    # to disk in settings.SALT_CLOUD_PROVIDERS_FILE
    yaml = models.TextField()

    # Where on disk is the private key going to be stored for this
    # cloud provider?
    private_key_file = DeletingFileField(max_length=255,
        upload_to=get_private_key_file_path,
        null=False,
        blank=False,
        storage=FileSystemStorage(location=settings.FILE_STORAGE_DIRECTORY))

    def __unicode__(self):

        return self.title

class CloudProviderInstanceSize(TitleSlugDescriptionModel):
    

    # `title` field will be the type used by salt-cloud for the `size` 
    # parameter in the providers yaml file (e.g., 'Micro Instance' or
    # '512MB Standard Instance'

    # link to the type of provider for this instance size
    provider_type = models.ForeignKey('CloudProviderType')

    # The underlying size ID of the instance (e.g., t1.micro)
    instance_id = models.CharField(max_length=64)

    def __unicode__(self):
        
        return '{0} ({1})'.format(self.title, self.instance_id)

class CloudProfile(TimeStampedModel, TitleSlugDescriptionModel):
    

    # Script choices available to the `script` field
    SCRIPT_CHOICES = (
        ('Ubuntu',)*2,
        ('RHEL5',)*2,
        ('RHEL6',)*2,
        ('Fedora',)*2,
    )
    # What cloud provider is this under?
    cloud_provider = models.ForeignKey('CloudProvider')
    
    # The underlying image id of this profile (e.g., ami-38df83a')
    image_id = models.CharField(max_length=64)

    # The default instance size of this profile, may be overridden
    # by the user at creation time
    default_instance_size = models.ForeignKey('CloudProviderInstanceSize')

    # The salt-cloud `script` parameter. Will most likely correspond to the
    # type of OS for this profile (e.g., Ubuntu, RHEL6, Fedora, etc)
    script = models.CharField(max_length=64, choices=SCRIPT_CHOICES)

    # The SSH user that will have default access to the box. Salt-cloud 
    # needs this to provision the box as a salt-minion and connect it
    # up to the salt-master automatically.
    ssh_user = models.CharField(max_length=64)

    def __unicode__(self):

        return self.title
