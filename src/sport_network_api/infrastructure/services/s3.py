class S3Service:
    def __init__(self, bucket: str, endpoint: str):
        self.bucket = bucket
        self.endpoint = endpoint

    async def upload_file(self, key: str, file_bytes: bytes) -> str:
        # TODO: Implement S3 upload
        pass

    async def delete_file(self, key: str) -> None:
        # TODO: Implement S3 delete
        pass

    async def get_url(self, key: str, expires_in: int = 3600) -> str:
        # TODO: Implement presigned URL
        pass

    async def upload_avatar(self, user_id: int, file_bytes: bytes) -> str:
        # TODO: Implement avatar upload
        pass

    def _generate_unique_filename(self, filename: str) -> str:
        # TODO: Implement
        pass

    def _validate_file(self, file_bytes: bytes, content_type: str) -> None:
        # TODO: Implement validation
        pass
