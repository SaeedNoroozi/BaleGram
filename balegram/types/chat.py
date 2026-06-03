from typing import Optional
from .base import BaleObject
from .chat_member import ChatMember

class Chat(BaleObject):
    def __init__(self, client, data: dict):
        self._client = client
        self.original_data: dict = data

        self.id: int = data.get("id")
        self.type: str = data.get("type", "private")
        self.title: Optional[str] = data.get("title")
        self.username: Optional[str] = data.get("username")
        self.first_name: Optional[str] = data.get("first_name")
        self.last_name: Optional[str] = data.get("last_name")
        self.description: Optional[str] = data.get("description")
        self.invite_link: Optional[str] = data.get("invite_link")

    @property
    def is_private(self) -> bool:
        return self.type == "private"

    @property
    def is_group(self) -> bool:
        return self.type == "group"
    
    @property
    def is_channel(self) -> bool:
        return self.type == "channel"

    async def leave(self) -> bool:
        return await self._client.leave_chat(self.id)

    async def get_administrators(self) -> list[ChatMember]:
        return await self._client.get_chat_administrators(self.id)
