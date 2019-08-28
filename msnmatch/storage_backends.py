from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from whitenoise.storage import CompressedManifestStaticFilesStorage


class WhiteNoiseStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

    def __init__(self, *args, **kwargs):
        kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
        super(MediaStorage, self).__init__(*args, **kwargs)

class StaticStorage(S3Boto3Storage):
    location = settings.BUILD_VERSION + '/static' 

    def __init__(self, *args, **kwargs):
        kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
        super(StaticStorage, self).__init__(*args, **kwargs)