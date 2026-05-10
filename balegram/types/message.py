import re
import os

from typing import Any, Dict, List, Optional

from .attachments import Contact, Location
from .base import BaleObject
from .chat import Chat
from .media import Animation, Audio, Document, PhotoSize, Video, Voice
from .user import User

class Message(BaleObject):
    def __init__(self, client, data: dict):
        self._client = client
        self.original_data: dict = data

        self.message_id: int = data.get("message_id") or data.get("id")
        self.date: int = data.get("date")

        sender_data = data.get("from", {})
        chat_data = data.get("chat", {})

        self.sender: Optional[User] = User(sender_data) if sender_data else None
        self.chat: Optional[Chat] = Chat(chat_data) if chat_data else None

        self.chat_id: Optional[int] = self.chat.id if self.chat else None
        self.sender_id: Optional[int] = self.sender.id if self.sender else None

        self.text: str = data.get("text", "")
        self.raw_text: str = self.text
        self.caption: Optional[str] = data.get("caption")

        if not self.text and self.caption:
            self.raw_text = self.caption

        self.edit_date: Optional[int] = data.get("edit_date")
        self.entities: Optional[List[Dict[str, Any]]] = data.get("entities")
        self.caption_entities: Optional[List[Dict[str, Any]]] = data.get("caption_entities")
        self.pattern_match: Optional[re.Match] = None

        self.forward_from: Optional[User] = User(data.get("forward_from")) if data.get("forward_from") else None
        self.forward_from_chat: Optional[Chat] = Chat(data.get("forward_from_chat")) if data.get("forward_from_chat") else None
        self.forward_from_message_id: Optional[int] = data.get("forward_from_message_id")
        self.forward_signature: Optional[str] = data.get("forward_signature")
        self.forward_sender_name: Optional[str] = data.get("forward_sender_name")
        self.forward_date: Optional[int] = data.get("forward_date")

        reply_data = data.get("reply_to_message")
        pinned_data = data.get("pinned_message")

        self.reply_to_message: Optional[Message] = Message(self._client, reply_data) if reply_data else None
        self.pinned_message: Optional[Message] = Message(self._client, pinned_data) if pinned_data else None

        photo_data = data.get("photo")
        self.photo: Optional[List[PhotoSize]] = [PhotoSize(photo) for photo in photo_data] if photo_data else None

        self.document: Optional[Document] = Document(data.get("document")) if data.get("document") else None
        self.video: Optional[Video] = Video(data.get("video")) if data.get("video") else None
        self.audio: Optional[Audio] = Audio(data.get("audio")) if data.get("audio") else None
        self.voice: Optional[Voice] = Voice(data.get("voice")) if data.get("voice") else None
        self.animation: Optional[Animation] = Animation(data.get("animation")) if data.get("animation") else None

        self.contact: Optional[Contact] = Contact(data.get("contact")) if data.get("contact") else None
        self.location: Optional[Location] = Location(data.get("location")) if data.get("location") else None

        new_members = data.get("new_chat_members")
        self.new_chat_members: Optional[List[User]] = [User(member) for member in new_members] if new_members else None
        self.left_chat_member: Optional[User] = User(data.get("left_chat_member")) if data.get("left_chat_member") else None

        self.new_chat_title: Optional[str] = data.get("new_chat_title")
        self.new_chat_photo: Optional[List[dict]] = data.get("new_chat_photo")
        self.delete_chat_photo: bool = data.get("delete_chat_photo")
        self.group_chat_created: bool = data.get("group_chat_created")


    @property
    def is_private(self) -> bool:
        return bool(self.chat and self.chat.is_private)
    
    @property
    def is_group(self) -> bool:
        return bool(self.chat and self.chat.is_group)
    
    @property
    def is_channel(self) -> bool:
        return bool(self.chat and self.chat.is_channel)

    @property
    def file(self):
        if self.photo:
            return self.photo[-1]
        if self.video:
            return self.video
        if self.audio:
            return self.audio
        if self.voice:
            return self.voice
        if self.animation:
            return self.animation
        if self.document:
            return self.document

        return None

    async def reply(
        self,
        message: Optional[str] = None,
        file: Any = None,
        caption: Optional[str] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ):
        target_message_id = self.message_id

        if file is not None:
            file_caption = caption or message

            ext = ""

            if isinstance(file, str):
                ext = os.path.splitext(file)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png', '.webp', '.bmp']:
                    return await self._client.send_photo(
                        entity=self.chat_id,
                        photo=file,
                        caption=file_caption,
                        reply_to=target_message_id,
                        reply_markup=reply_markup
                    )
                elif ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv']:
                    return await self._client.send_video(
                        entity=self.chat_id,
                        video=file,
                        caption=file_caption,
                        reply_to=target_message_id,
                        reply_markup=reply_markup
                    )
                elif ext == '.ogg':
                    return await self._client.send_voice(
                        entity=self.chat_id,
                        voice=file,
                        caption=file_caption,
                        reply_to=target_message_id,
                        reply_markup=reply_markup
                    )
                elif ext in ['.mp3', '.wav', '.m4a', '.aac']:
                    return await self._client.send_audio(
                        entity=self.chat_id,
                        audio=file,
                        caption=file_caption,
                        reply_to=target_message_id,
                        reply_markup=reply_markup
                    )
                elif ext in ['.gif']:
                    return await self._client.send_animation(
                        entity=self.chat_id,
                        animation=file,
                        caption=file_caption,
                        reply_to=target_message_id,
                        reply_markup=reply_markup
                    )
                else:
                    return await self._client.send_document(
                        entity=self.chat_id,
                        document=file,
                        caption=file_caption,
                        reply_to=target_message_id,
                        reply_markup=reply_markup
                    )
                
        return await self._client.send_message(
            entity=self.chat_id,
            message=message or "",
            reply_to=target_message_id,
            reply_markup=reply_markup
        )
