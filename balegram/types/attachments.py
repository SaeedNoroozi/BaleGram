from typing import Optional
from .base import BaleObject

class Contact(BaleObject):
    def __init__(self, data: dict):
        self.original_data: dict = data
        
        self.phone_number: str = data.get("phone_number")
        self.first_name: str = data.get("first_name")
        self.last_name: Optional[str] = data.get("last_name")
        self.user_id: Optional[int] = data.get("user_id")

class Location(BaleObject):
    def __init__(self, data: dict):
        self.original_data: dict = data
        
        self.longitude: float = data.get("longitude")
        self.latitude: float = data.get("latitude")