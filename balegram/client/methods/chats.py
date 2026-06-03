from typing import Union, List, Optional
from balegram.types.chat import Chat
from balegram.types.chat_member import ChatMember
from balegram.types.chat_invite_link import ChatInviteLink

import os
import aiohttp
import mimetypes

class ChatsMethods:

    async def get_chat(self, chat_id: Union[int, str]) -> Chat:
        payload = {
            "chat_id": str(chat_id),
        }
        response = await self._request("getChat", data=payload)
        return Chat(self, response.get("result", response))

    async def get_chat_administrators(self, chat_id: Union[int, str]) -> List[ChatMember]:
        payload = {
            "chat_id": str(chat_id),
        }
        response = await self._request("getChatAdministrators", data=payload)
        return [ChatMember(admin) for admin in response.get("result", [])]
    
    async def ban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str],
    ) -> bool:
        payload = {
            "chat_id": str(chat_id),
            "user_id": str(user_id),
        }
        response = await self._request("banChatMember", data=payload)
        return response.get("result", False)
    
    async def unban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str],
        only_if_banned: bool = True,
    ) -> bool:
        payload = {
            "chat_id": str(chat_id),
            "user_id": str(user_id),
            "only_if_banned": only_if_banned,
        }
        response = await self._request("unbanChatMember", data=payload)
        return response.get("result", False)
    
    async def leave_chat(
        self,
        chat_id: Union[int, str],
    ) -> bool:
        payload = {
            "chat_id": str(chat_id),
        }
        response = await self._request("leaveChat", data=payload)
        return response.get("result", False)
    
    async def get_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str],
    ) -> ChatMember:
        payload = {
            "chat_id": str(chat_id),
            "user_id": str(user_id),
        }
        response = await self._request("getChatMember", data=payload)
        return ChatMember(response.get("result", response))
    
    async def get_chat_member_count(
        self,
        chat_id: Union[int, str],
    ) -> int:
        payload = {
            "chat_id": str(chat_id),
        }
        response = await self._request("getChatMemberCount", data=payload)
        return response.get("result", 0)
    
    async def set_chat_title(
        self,
        chat_id: Union[int, str],
        title: str,
    ) -> bool:
        payload = {
            "chat_id": str(chat_id),
            "title": title,
        }
        response = await self._request("setChatTitle", data=payload)
        return response.get("result", False)
    
    async def set_chat_description(
        self,
        chat_id: Union[int, str],
        description: str,
    ) -> bool:
        payload = {
            "chat_id": str(chat_id),
            "description": description,
        }
        response = await self._request("setChatDescription", data=payload)
        return response.get("result", False)
    
    async def set_chat_photo(
        self,
        chat_id: Union[int, str],
        photo: str,
    ) -> bool:
        if not os.path.isfile(photo):
            raise FileNotFoundError(f"File not found: {photo}")
        
        content_type, _ = mimetypes.guess_type(photo)
        content_type = content_type or "application/octet-stream"
        
        with open(photo, "rb") as f:
            form_data = aiohttp.FormData()
            form_data.add_field("chat_id", str(chat_id))

            form_data.add_field(
                "photo",
                f,
                filename=os.path.basename(photo),
                content_type=content_type,
            )

            response = await self._request("setChatPhoto", data=form_data, is_multipart=True)
            return response.get("result", False)

    async def delete_chat_photo(
        self,
        chat_id: Union[int, str],
    ) -> bool:
        payload = {
            "chat_id": str(chat_id),
        }
        response = await self._request("deleteChatPhoto", data=payload)
        return response.get("result", False)

    async def promote_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str],
        is_anonymous: Optional[bool] = None,
        can_manage_chat: Optional[bool] = None,
        can_change_info: Optional[bool] = None,
        can_post_messages: Optional[bool] = None,
        can_edit_messages: Optional[bool] = None,
        can_delete_messages: Optional[bool] = None,
        can_manage_video_chats: Optional[bool] = None,
        can_restrict_members: Optional[bool] = None,
        can_promote_members: Optional[bool] = None,
        can_invite_users: Optional[bool] = None,
        can_pin_messages: Optional[bool] = None,
        can_manage_topics: Optional[bool] = None,
        can_post_stories: Optional[bool] = None,
        can_edit_stories: Optional[bool] = None,
        can_delete_stories: Optional[bool] = None,
    ) -> bool:
        payload = {
            "chat_id": str(chat_id),
            "user_id": str(user_id),
        }

        permissions = {
            "is_anonymous": is_anonymous,
            "can_manage_chat": can_manage_chat,
            "can_change_info": can_change_info,
            "can_post_messages": can_post_messages,
            "can_edit_messages": can_edit_messages,
            "can_delete_messages": can_delete_messages,
            "can_manage_video_chats": can_manage_video_chats,
            "can_restrict_members": can_restrict_members,
            "can_promote_members": can_promote_members,
            "can_invite_users": can_invite_users,
            "can_pin_messages": can_pin_messages,
            "can_manage_topics": can_manage_topics,
            "can_post_stories": can_post_stories,
            "can_edit_stories": can_edit_stories,
            "can_delete_stories": can_delete_stories,
        }
        
        for key, value in permissions.items():
            if value is not None:
                payload[key] = value

        response = await self._request("promoteChatMember", data=payload)
        return response.get("result", False)
    
    async def pin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
    ) -> bool:
        payload = {
            "chat_id": str(chat_id),
            "message_id": message_id,
        }
        response = await self._request("pinChatMessage", data=payload)
        return response.get("result", False)
    
    async def unpin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
    ) -> bool:
        payload = {
            "chat_id": str(chat_id),
            "message_id": message_id,
        }
        response = await self._request("unPinChatMessage", data=payload)
        return response.get("result", False)

    async def unpin_all_chat_messages(
        self,
        chat_id: Union[int, str],
    ) -> bool:
        payload = {
            "chat_id": str(chat_id),
        }
        response = await self._request("unpinAllChatMessages", data=payload)
        return response.get("result", False)
    
    async def create_chat_invite_link(
        self,
        chat_id: Union[int, str],
    ) -> ChatInviteLink:
        payload = {
            "chat_id": str(chat_id),
        }
        response = await self._request("createChatInviteLink", data=payload)
        return ChatInviteLink(response.get("result", {}))
    
    # async def create_chat_invite_link(
    #     self,
    #     chat_id: Union[int, str],
    #     name: Optional[str] = None,
    #     expire_date: Optional[int] = None,
    #     member_limit: Optional[int] = None,
    #     creates_join_request: Optional[bool] = None,
    # ) -> ChatInviteLink:
    #     payload = {
    #         "chat_id": str(chat_id),
    #     }

    #     if name:
    #         payload["name"] = name
    #     if expire_date:
    #         payload["expire_date"] = expire_date
    #     if member_limit:
    #         payload["member_limit"] = member_limit
    #     if creates_join_request:
    #         payload["creates_join_request"] = creates_join_request

    #     response = await self._request("createChatInviteLink", data=payload)

    #     return ChatInviteLink(response.get("result", {}))

    async def revoke_chat_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
    ) -> bool:
        payload = {
            "chat_id": str(chat_id),
            "invite_link": invite_link,
        }
        response = await self._request("revokeChatInviteLink", data=payload)
        return response.get("result", False)
    
    async def export_chat_invite_link(
        self,
        chat_id: Union[int, str],
    ) -> str:
        payload = {
            "chat_id": str(chat_id),
        }
        response = await self._request("exportChatInviteLink", data=payload)
        return response.get("result", "")
    