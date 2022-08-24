from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    inherit from django storages and store static files in a location
    defined in settings
    """
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """
    inherit from django storages and store media files in a location
    defined in settings
    """
    location = settings.MEDIAFILES_LOCATION