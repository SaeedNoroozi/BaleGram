from typing import Any, Optional, Union

import json

class MessagesMethods:

    def _parse_markup(self, markup: Any) -> Any:
        if hasattr(markup, "to_dict"):
            return markup.to_dict()
        elif isinstance(markup, dict):
            return json.dumps(markup)
        else:
            raise ValueError("Invalid reply markup type")

    async def send_message(
        self,
        entity: Union[int, str],
        message: str,
        reply_to: Optional[int] = None,
        reply_markup: Optional[Any] = None,
    ):
        payload = {
            "chat_id": entity,
            "text": str(message),
        }

        if reply_to is not None:
            payload["reply_to_message_id"] = reply_to

        if reply_markup is not None:
            payload["reply_markup"] = self._parse_markup(reply_markup)

        response: Any = await self._request("sendMessage", data=payload)

        if response and response.get("ok"):
            from balegram.types.message import Message
            return Message(client=self, data=response["result"])
        
        return response
        
    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: Optional[str] = None,
        show_alert: bool = False,
    ):
        payload = {
            "callback_query_id": callback_query_id,
            "show_alert": show_alert,
        }

        if text:
            payload["text"] = text

        return await self._request("answerCallbackQuery", data=payload)

    async def edit_message_text(
        self,
        entity: Union[int, str],
        message_id: int,
        text: str,
        reply_markup: Optional[Any] = None,
    ):
        payload = {
            "chat_id": entity,
            "message_id": message_id,
            "text": text,
        }

        if reply_markup is not None:
            payload["reply_markup"] = self._parse_markup(reply_markup)

        response = await self._request("editMessageText", data=payload)

        if response and response.get("ok"):
            if isinstance(response["result"], dict) and "message_id" in response["result"]:
                from balegram.types.message import Message
                return Message(client=self, data=response["result"])
            else:
                return response["result"]
        
        return response
    
    async def edit_message_caption(
        self,
        entity: Union[int, str],
        message_id: int,
        caption: str,
        reply_markup: Optional[Any] = None,
    ):
        payload = {
            "chat_id": entity,
            "message_id": message_id,
            "caption": caption,
        }

        if reply_markup is not None:
            payload["reply_markup"] = self._parse_markup(reply_markup)

        response = await self._request("editMessageCaption", data=payload)

        if response and response.get("ok"):
            if isinstance(response["result"], dict) and "message_id" in response["result"]:
                from balegram.types.message import Message
                return Message(client=self, data=response["result"])
            else:
                return response["result"]
        
        return response
    
    async def edit_message_reply_markup(
        self,
        entity: Union[int, str],
        message_id: int,
        reply_markup: Optional[Any] = None,
    ):
        payload = {
            "chat_id": entity,
            "message_id": message_id,
        }

        if reply_markup is not None:
            payload["reply_markup"] = self._parse_markup(reply_markup)

        response = await self._request("editMessageReplyMarkup", data=payload)

        if response and response.get("ok"):
            if isinstance(response["result"], dict) and "message_id" in response["result"]:
                from balegram.types.message import Message
                return Message(client=self, data=response["result"])
            else:
                return response["result"]
        
        return response
    
    async def delete_message(
        self,
        entity: Union[int, str],
        message_id: int,
    ):
        payload = {
            "chat_id": entity,
            "message_id": message_id,
        }

        response = await self._request("deleteMessage", data=payload)

        return response.get("result", False)

    async def forward_message(
        self,
        entity: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
    ):

        payload = {
            "chat_id": entity,
            "from_chat_id": from_chat_id,
            "message_id": message_id,
        }

        response = await self._request("forwardMessage", data=payload)

        if response and response.get("ok"):
            from balegram.types.message import Message
            return Message(client=self, data=response["result"])
        
        return response

    async def copy_message(
        self,
        entity: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
    ):
        payload = {
            "chat_id": entity,
            "from_chat_id": from_chat_id,
            "message_id": message_id,
        }

        response = await self._request("copyMessage", data=payload)

        if response and response.get("ok"):
            return response["result"]
        
        return response

    async def send_location(
        self,
        entity: Union[int, str],
        latitude: float,
        longitude: float,
        horizontal_accuracy: Optional[float] = None,
        reply_to: Optional[int] = None,
        reply_markup: Optional[Any] = None,
    ):
        payload = {
            "chat_id": entity,
            "latitude": latitude,
            "longitude": longitude,
        }

        if reply_to is not None:
            payload["reply_to_message_id"] = reply_to

        if horizontal_accuracy is not None:
            payload["horizontal_accuracy"] = horizontal_accuracy

        if reply_markup is not None:
            payload["reply_markup"] = self._parse_markup(reply_markup)

        response = await self._request("sendLocation", data=payload)

        if response and response.get("ok"):
            from balegram.types.message import Message
            return Message(client=self, data=response["result"])
        
        return response

    async def send_contact(
        self,
        entity: Union[int, str],
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        reply_to: Optional[int] = None,
        reply_markup: Optional[Any] = None,
    ):
        payload = {
            "chat_id": entity,
            "phone_number": str(phone_number),
            "first_name": str(first_name),
        }

        if last_name is not None:
            payload["last_name"] = str(last_name)

        if reply_to is not None:
            payload["reply_to_message_id"] = reply_to

        if reply_markup is not None:
            payload["reply_markup"] = self._parse_markup(reply_markup)

        response = await self._request("sendContact", data=payload)

        if response and response.get("ok"):
            from balegram.types.message import Message
            return Message(client=self, data=response["result"])
        
        return response

    async def send_chat_action(
        self,
        entity: Union[int, str],
        action: str,
    ):
        """
        Sends a chat action to the user.
        Supported actions: 
        - 'typing': The user is typing.
        - 'upload_photo': The user is uploading a photo.
        - 'upload_video': The user is uploading a video.
        - 'record_video': The user is recording a video.
        - 'record_voice': The user is recording a voice.
        - 'upload_voice': The user is uploading a voice.
        - 'choose_sticker': The user is choosing a sticker.
        """
        payload = {
            "chat_id": str(entity),
            "action": action,
        }

        response = await self._request("sendChatAction", data=payload)

        return response.get("result", False)


