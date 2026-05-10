import os

from typing import Any, Dict, Optional
from .base import BaleObject
from .user import User
from .message import Message

class CallbackQueryEvent(BaleObject):

    def __init__(self, client, data: dict):
        self._client = client
        self.original_data: dict = data

        self.id: str = data.get("id")
        self.sender: Optional[User] = User(data.get("from")) if data.get("from") else None
        self.data: Optional[str] = data.get("data")

        self.message: Optional[Message] = Message(client, data.get("message")) if data.get("message") else None

        self.chat_id: Optional[int] = self.message.chat.id if self.message else None
        self.sender_id: Optional[int] = self.sender.id if self.sender else None

    async def answer(self, text: Optional[str] = None, show_alert: bool = False):
        return await self._client.answer_callback_query(self.id, text, show_alert)

    async def reply(
        self,
        message: Optional[str] = None,
        file: Any = None,
        caption: Optional[str] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ):
        target_message_id = getattr(self, "message_id", None)
        if hasattr(self, "message") and self.message:
            target_message_id = self.message.message_id

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
