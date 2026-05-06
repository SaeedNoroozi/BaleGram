from typing import Optional
from .base import BaleObject

class PhotoSize(BaleObject):
    def __init__(self, data: dict):
        self.original_data: dict = data

        self.file_id: str = data.get("file_id")
        self.file_unique_id: str = data.get("file_unique_id")
        self.width: int = data.get("width")
        self.height: int = data.get("height")
        self.file_size: Optional[int] = data.get("file_size")

class Video(BaleObject):
    def __init__(self, data: dict):
        self.original_data: dict = data

        self.file_id: str = data.get("file_id")
        self.file_unique_id: str = data.get("file_unique_id")
        self.width: int = data.get("width")
        self.height: int = data.get("height")
        self.duration: int = data.get("duration")
        self.mime_type: Optional[str] = data.get("mime_type")
        self.file_size: Optional[int] = data.get("file_size")

class Document(BaleObject):
    def __init__(self, data: dict):
        self.original_data: dict = data

        self.file_id: str = data.get("file_id")
        self.file_unique_id: str = data.get("file_unique_id")
        self.file_name: Optional[str] = data.get("file_name")
        self.mime_type: Optional[str] = data.get("mime_type")
        self.file_size: Optional[int] = data.get("file_size")
        self.thumbnail: Optional[PhotoSize] = PhotoSize(data.get("thumbnail")) if data.get("thumbnail") else None

class Animation(BaleObject):
    def __init__(self, data: dict):
        self.original_data: dict = data

        self.file_id: str = data.get("file_id")
        self.file_unique_id: str = data.get("file_unique_id")
        self.width: int = data.get("width")
        self.height: int = data.get("height")
        self.duration: int = data.get("duration")
        self.file_size: Optional[int] = data.get("file_size")
        self.thumbnail: Optional[PhotoSize] = PhotoSize(data.get("thumbnail")) if data.get("thumbnail") else None
        self.file_name: Optional[str] = data.get("file_name")
        self.mime_type: Optional[str] = data.get("mime_type")

class Voice(BaleObject):
    def __init__(self, data: dict):
        self.original_data: dict = data

        self.file_id: str = data.get("file_id")
        self.file_unique_id: str = data.get("file_unique_id")

class Audio(BaleObject):
    def __init__(self, data: dict):
        self.original_data: dict = data

        self.file_id: str = data.get("file_id")
        self.file_unique_id: str = data.get("file_unique_id")
        self.duration: int = data.get("duration")
        self.title: Optional[str] = data.get("title")
        self.file_name: Optional[str] = data.get("file_name")
        self.mime_type: Optional[str] = data.get("mime_type")
        self.file_size: Optional[int] = data.get("file_size")
