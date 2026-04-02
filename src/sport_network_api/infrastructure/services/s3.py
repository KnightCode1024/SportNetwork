class S3Service:
    def __init__():
        pass
    
    async def upload_file() -> str:
        pass
    
    async def delete_file(self, key: str) -> None:
        pass
    
    async def get_url(self, key: str, expires_in: int = 3600) -> str:
        pass
    
    async def upload_avatar() -> str:
        pass
    
    def _generate_unique_filename(self, filename: str) -> str:
        pass
    
    def _validate_file(self, file_bytes: bytes, content_type: str) -> None:
        pass
