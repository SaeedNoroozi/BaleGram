import os
import aiofiles

from balegram.errors import FileTooLargeError, FileDownloadError, LocalFileSystemError
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

    async def get_file(self, file_id: str):
        payload = {
            "file_id": file_id,
        }

        response = await self._request("getFile", data=payload)

        if response and response.get("ok"):
            from balegram.types.file import File
            return File(client=self, data=response["result"])
        
        return response

    async def download_file(self, file_id: str, save_path: str) -> str:
        file_object = await self.get_file(file_id)

        save_dir = os.path.dirname(save_path)
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)

        if not hasattr(file_object, "file_path") or not file_object.file_path:
            raise FileDownloadError(f"Could not find file_path for file_id: {file_id}. Make sure the ID is correct.")

        if file_object.file_size and file_object.file_size > (20 * 1024 * 1024):
            mb_size = file_object.file_size / (1024 * 1024)
            raise FileTooLargeError(f"File size is too large to download. The file is {mb_size:.2f} MB. The maximum allowed size is 20 MB.")

        base_api_url = self.base_url.split("/bot")[0]
        download_url = f"{base_api_url}/file/bot{self.token}/{file_object.file_path}"

        try:
            async with self._session.get(download_url) as response:
                if response.status != 200:
                    raise FileDownloadError(f"Failed to download file. Status code: {response.status}")
                
                async with aiofiles.open(save_path, "wb") as f:
                    async for chunk in response.content.iter_chunked(1024 * 1024):
                        await f.write(chunk)
        
        except FileNotFoundError:
            raise LocalFileSystemError(f"Could not find file at path: {save_path}")
        
        except Exception as e:
            raise FileDownloadError(f"Failed to download file: {e}")

        return save_path

