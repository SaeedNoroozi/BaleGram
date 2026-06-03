from typing import Optional
from .base import BaleObject
from .user import User

class ChatInviteLink(BaleObject):

    def __init__(self, data: dict):
        self.original_data: dict = data

        self.invite_link: str = data.get("invite_link")

        creator_data: dict = data.get("creator", {})
        self.creator: Optional[User] = User(creator_data) if creator_data else None

        self.creates_join_request: bool = data.get("creates_join_request", False)
        self.is_primary: bool = data.get("is_primary", False)
        self.is_revoked: bool = data.get("is_revoked", False)
        self.name: str = data.get("name", "")
        

        self.expire_date: int = data.get("expire_date", 0)
        self.member_limit: int = data.get("member_limit", 0)
        self.pending_join_request_count: int = data.get("pending_join_request_count", 0)
