from typing import Optional
from .base import BaleObject
from .user import User

class ChatMember(BaleObject):

    def __init__(self, data: dict):
        self.original_data: dict = data

        self.status: str = data.get("status", "")
        
        user_data = data.get("user", {})
        self.user: User = User(user_data)

        self.can_be_edited: Optional[bool] = data.get("can_be_edited")
        self.is_anonymous: Optional[bool] = data.get("is_anonymous")
        self.can_manage_chat: Optional[bool] = data.get("can_manage_chat")
        self.can_change_info: Optional[bool] = data.get("can_change_info")
        self.can_delete_messages: Optional[bool] = data.get("can_delete_messages")
        self.can_invite_users: Optional[bool] = data.get("can_invite_users")
        self.can_restrict_members: Optional[bool] = data.get("can_restrict_members")
        self.can_promote_members: Optional[bool] = data.get("can_promote_members")
        self.can_manage_video_chats: Optional[bool] = data.get("can_manage_video_chats")

        self.can_pin_messages: Optional[bool] = data.get("can_pin_messages")
        self.can_manage_topics: Optional[bool] = data.get("can_manage_topics")

        self.can_post_messages: Optional[bool] = data.get("can_post_messages")
        self.can_edit_messages: Optional[bool] = data.get("can_edit_messages")
        self.can_post_stories: Optional[bool] = data.get("can_post_stories")
        self.can_edit_stories: Optional[bool] = data.get("can_edit_stories")
        self.can_delete_stories: Optional[bool] = data.get("can_delete_stories")

    @property
    def is_admin(self) -> bool:
        return self.status in ["creator", "administrator"]
    
    @property
    def is_owner(self) -> bool:
        return self.status == "creator"
    
    @property
    def is_member(self) -> bool:
        return self.status == "member"
