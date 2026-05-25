from typing import Protocol


class S3ServiceInterface(Protocol):
    async def upload_avatar(
        self,
        user_id: int,
        file_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> str:
        ...

    async def delete_file(self, key: str) -> None:
        ...

    def get_key_from_url(self, url: str) -> str | None:
        ...
