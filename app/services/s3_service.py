import logging

import boto3
from django.conf import settings

logger = logging.getLogger(__name__)


class S3Service:
    def __init__(self):
        self.s3_client = self._get_s3_client()

    def _get_s3_client(self):
        return boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

    def generate_presigned_url(self, *, file_path: str, file_type: str):
        acl = settings.AWS_DEFAULT_ACL
        expires_in = int(settings.AWS_PRESIGNED_EXPIRE)

        logger.info(f"Generating presigned URL for {file_path}")
        presigned_data = self.s3_client.generate_presigned_post(
            settings.AWS_STORAGE_BUCKET_NAME,
            file_path,
            Fields={
                "acl": acl,
                "Content-Type": file_type,
            },
            Conditions=[
                {"acl": acl},
                {"Content-Type": file_type},
            ],
            ExpiresIn=expires_in,
        )

        return presigned_data

    def download_file(self, key: str, local_path: str):
        logger.info(f"Downloading document {key}")

        self.s3_client.download_file(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key, Filename=local_path)

        logger.info(f"Downloaded document {local_path}")
