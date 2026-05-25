import json
from pathlib import Path
from uuid import uuid4

import aioboto3


class S3Gateway:
    allowed_content_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
    }
    max_avatar_size_bytes = 5 * 1024 * 1024

    def __init__(
        self,
        bucket: str,
        endpoint: str,
        public_endpoint: str,
        access_key: str,
        secret_key: str,
        region: str,
    ):
        self.bucket = bucket
        self.endpoint = endpoint.rstrip("/")
        self.public_endpoint = public_endpoint.rstrip("/")
        self.region = region
        self._client_kwargs = {
            "endpoint_url": self.endpoint,
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "region_name": region,
        }
        self._session = aioboto3.Session()

    def _create_client(self):
        return self._session.client("s3", **self._client_kwargs)

    async def upload_file(
        self,
        key: str,
        file_bytes: bytes,
        content_type: str = "application/octet-stream",
    ) -> str:
        await self._ensure_bucket_exists()
        async with await self._create_client() as client:
            await client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=file_bytes,
                ContentType=content_type,
            )
        return self._build_public_url(key)

    async def delete_file(self, key: str) -> None:
        async with await self._create_client() as client:
            await client.delete_object(Bucket=self.bucket, Key=key)

    async def get_url(self, key: str, expires_in: int = 3600) -> str:
        async with self._create_client() as client:
            return client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": key},
                ExpiresIn=expires_in,
            )

    async def upload_avatar(
        self,
        user_id: int,
        file_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> str:
        self._validate_file(file_bytes, content_type)
        unique_filename = self._generate_unique_filename(filename)
        key = f"avatars/{user_id}/{unique_filename}"
        return await self.upload_file(key, file_bytes, content_type)

    def get_key_from_url(self, url: str) -> str | None:
        prefix = f"{self.public_endpoint}/"
        if not url.startswith(prefix):
            return None
        return url.removeprefix(prefix)

    async def _ensure_bucket_exists(self) -> None:
        async with self._create_client() as client:
            try:
                await client.head_bucket(Bucket=self.bucket)
            except Exception as err:
                error_code = None
                if hasattr(err, "response"):
                    error_code = err.response.get("Error", {}).get("Code")
                if error_code not in {"404", "NoSuchBucket"}:
                    raise

                create_kwargs = {"Bucket": self.bucket}
                if self.region != "us-east-1":
                    create_kwargs["CreateBucketConfiguration"] = {
                        "LocationConstraint": self.region,
                    }
                await client.create_bucket(**create_kwargs)

            bucket_policy = json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "PublicReadGetObject",
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": ["s3:GetObject"],
                            "Resource": [f"arn:aws:s3:::{self.bucket}/*"],
                        }
                    ],
                }
            )
            await client.put_bucket_policy(Bucket=self.bucket, Policy=bucket_policy)

    def _build_public_url(self, key: str) -> str:
        return f"{self.public_endpoint}/{key}"

    def _generate_unique_filename(self, filename: str) -> str:
        suffix = Path(filename).suffix.lower()
        if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
            suffix = ".jpg"
        return f"{uuid4().hex}{suffix}"

    def _validate_file(self, file_bytes: bytes, content_type: str) -> None:
        if not file_bytes:
            raise ValueError("Avatar file is empty")
        if content_type not in self.allowed_content_types:
            raise ValueError("Unsupported avatar format")
        if len(file_bytes) > self.max_avatar_size_bytes:
            raise ValueError("Avatar file is too large")
