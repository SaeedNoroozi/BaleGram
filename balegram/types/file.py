from typing import Optional
from .base import BaleObject

class File(BaleObject):
    def __init__(self, client, data: dict):
        self._client = client
        self.original_data: dict = data

        self.file_id: str = data.get("file_id")
        self.file_unique_id: str = data.get("file_unique_id")
        self.file_size: int = data.get("file_size")
        self.file_path: str = data.get("file_path")

    async def download(self, save_path: str):
        return await self._client.download_file(self.file_id, save_path)