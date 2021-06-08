from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False

class PublicImagesStorage(S3Boto3Storage):
    location = 'images'
    default_acl = 'public-read'
    file_overwrite = False
   

class PublicFilesStorage(S3Boto3Storage):
    location = 'files'
    default_acl = 'public-read'
    file_overwrite = False
   

class PublicVideosStorage(S3Boto3Storage):
    location = 'videos'
    default_acl = 'public-read'
    file_overwrite = False
   