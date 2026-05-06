from typing import Optional
from .base import BaleObject

class User(BaleObject):
    def __init__(self, data: dict):
        self.original_data: dict = data

        self.id: int = data.get("id")
        self.is_bot: bool = data.get("is_bot", False)
        self.first_name: str = data.get("first_name", "")
        self.last_name: Optional[str] = data.get("last_name")
        self.username: Optional[str] = data.get("username")
        self.language_code: Optional[str] = data.get("language_code")