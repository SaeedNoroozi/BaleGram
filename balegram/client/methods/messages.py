from typing import Any, Dict, Optional, Union

class MessagesMethods:

    async def send_message(
        self,
        entity: Union[int, str],
        message: str,
        reply_to: Optional[int] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ):
        payload = {
            "chat_id": entity,
            "text": str(message),
        }

        if reply_to is not None:
            payload["reply_to_message_id"] = reply_to

        if reply_markup is not None:
            payload["reply_markup"] = reply_markup

        response: Any = await self._request("sendMessage", data=payload)

        if response and response.get("ok"):
            from ...types.message import Message
            return Message(client=self, data=response["result"])
        
        return response