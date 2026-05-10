import os
from typing import Any, Dict, Optional, Union

import aiohttp
import json

class MediaMethods:

    async def _upload_file_send_id(
        self,
        method: str,
        entity: Union[int, str],
        file_field_name: str,
        file_data: Any,
        kwargs: dict,
    ):
        if "reply_markup" in kwargs and kwargs["reply_markup"] is not None:
            markup = kwargs["reply_markup"]
            if hasattr(markup, "to_dict"):
                kwargs["reply_markup"] = json.dumps(markup.to_dict())
            elif isinstance(markup, dict):
                kwargs["reply_markup"] = json.dumps(markup)
            else:
                raise ValueError("Invalid reply markup type")

        if isinstance(file_data, str) and os.path.isfile(file_data):
            form = aiohttp.FormData()
            form.add_field('chat_id', str(entity))

            for key, value in kwargs.items():
                if value is not None:
                    form.add_field(key, str(value))

            with open(file_data, "rb") as f:
                form.add_field(file_field_name, f)
                response = await self._request(method, data=form, is_multipart=True)

        else:
            payload = {
                "chat_id": str(entity),
                file_field_name: file_data,
            }

            for key, value in kwargs.items():
                if value is not None:
                    payload[key] = value

            response = await self._request(method, data=payload)

        if response and response.get("ok"):
            from balegram.types.message import Message
            return Message(client=self, data=response["result"])
        
        return response

    async def send_photo(
        self,
        entity: Union[int, str],
        photo: str,
        caption: Optional[str] = None,
        reply_to: Optional[int] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ):
        kwargs = {
            "caption": caption,
            "reply_to_message_id": reply_to,
            "reply_markup": reply_markup,
        }

        return await self._upload_file_send_id(
            "sendPhoto",
            entity,
            "photo",
            photo,
            kwargs,
        )

    async def send_video(
        self,
        entity: Union[int, str],
        video: str,
        caption: Optional[str] = None,
        reply_to: Optional[int] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ):
        kwargs = {
            "caption": caption,
            "reply_to_message_id": reply_to,
            "reply_markup": reply_markup,
        }

        return await self._upload_file_send_id(
            "sendVideo",
            entity,
            "video",
            video,
            kwargs,
        )

    async def send_document(
        self,
        entity: Union[int, str],
        document: str,
        caption: Optional[str] = None,
        reply_to: Optional[int] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ):
        kwargs = {
            "caption": caption,
            "reply_to_message_id": reply_to,
            "reply_markup": reply_markup,
        }

        return await self._upload_file_send_id(
            "sendDocument",
            entity,
            "document",
            document,
            kwargs,
        )

    async def send_audio(
        self,
        entity: Union[int, str],
        audio: str,
        caption: Optional[str] = None,
        reply_to: Optional[int] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ):
        kwargs = {
            "caption": caption,
            "reply_to_message_id": reply_to,
            "reply_markup": reply_markup,
        }

        return await self._upload_file_send_id(
            "sendAudio",
            entity,
            "audio",
            audio,
            kwargs,
        )

    async def send_voice(
        self,
        entity: Union[int, str],
        voice: str,
        caption: Optional[str] = None,
        reply_to: Optional[int] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ):
        kwargs = {
            "caption": caption,
            "reply_to_message_id": reply_to,
            "reply_markup": reply_markup,
        }

        return await self._upload_file_send_id(
            "sendVoice",
            entity,
            "voice",
            voice,
            kwargs,
        )

    async def send_animation(
        self,
        entity: Union[int, str],
        animation: str,
        caption: Optional[str] = None,
        reply_to: Optional[int] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ):
        kwargs = {
            "caption": caption,
            "reply_to_message_id": reply_to,
            "reply_markup": reply_markup,
        }

        return await self._upload_file_send_id(
            "sendAnimation",
            entity,
            "animation",
            animation,
            kwargs,
        )