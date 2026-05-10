from typing import Any, Dict, Optional, Union

import json

class MessagesMethods:

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
            if hasattr(reply_markup, "to_dict"):
                payload["reply_markup"] = reply_markup.to_dict()
            elif isinstance(reply_markup, dict):
                payload["reply_markup"] = json.dumps(reply_markup)
            else:
                raise ValueError("Invalid reply markup type")

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
