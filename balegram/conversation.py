import asyncio
from typing import Optional

class Conversation:

    def __init__(self, client, chat_id: str | int, timeout: int = 120):
        self._client = client
        self.chat_id = str(chat_id)
        self.timeout = timeout

        self._waiter: Optional[asyncio.Future] = None

    async def __aenter__(self):
        if self.chat_id in self._client._conversations:
            raise ValueError(f"Conversation already exists for chat {self.chat_id}")

        self._client._conversations[self.chat_id] = self
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self._client._conversations.pop(self.chat_id, None)

        if self._waiter and not self._waiter.done():
            self._waiter.cancel()

    async def send_message(self, message: str, **kwargs):
        return await self._client.send_message(self.chat_id, message, **kwargs)

    async def get_response(self):
        self._waiter = asyncio.Future()

        try:
            message = await asyncio.wait_for(self._waiter, self.timeout)
            self._waiter = None
            return message

        except asyncio.TimeoutError:
            self._waiter = None
            self._client._conversations.pop(self.chat_id, None)
            raise TimeoutError(f"Conversation timed out after {self.timeout} seconds")
