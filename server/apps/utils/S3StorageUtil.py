import os
import datetime
from django.conf import settings
from django.utils.deconstruct import deconstructible
import uuid
import requests

from boto.s3.connection import OrdinaryCallingFormat

from storages.backends.s3boto import S3BotoStorage


@deconstructible
class MyS3BotoStorage(S3BotoStorage):
    pass

StaticS3BotoStorage = lambda: MyS3BotoStorage(location='static')
MediaS3BotoStorage = lambda: MyS3BotoStorage(location='media')

media_bucket_name = getattr(settings, 'AWS_MEDIA_BUCKET_NAME')
protected_storage = MyS3BotoStorage(
  acl='private',
  querystring_auth=True,
  querystring_expire=600,
  bucket=media_bucket_name
)
