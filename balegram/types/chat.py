from typing import Optional
from .base import BaleObject

class Chat(BaleObject):
    def __init__(self, data: dict):
        self.original_data: dict = data

        self.id: int = data.get("id")
        self.type: str = data.get("type", "private")
        self.title: Optional[str] = data.get("title")
        self.username: Optional[str] = data.get("username")
        self.first_name: Optional[str] = data.get("first_name")
        self.last_name: Optional[str] = data.get("last_name")

    @property
    def is_private(self) -> bool:
        return self.type == "private"

    @property
    def is_group(self) -> bool:
        return self.type == "group"
    
    @property
    def is_channel(self) -> bool:
        return self.type == "channel"