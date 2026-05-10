import asyncio
import aiohttp
import traceback

from typing import Any, Awaitable, Callable, Optional, Tuple

from balegram.events import NewMessage, CallbackQuery
from balegram.types.message import Message
from balegram.types.callback_query import CallbackQueryEvent
from .methods.messages import MessagesMethods
from .methods.media import MediaMethods

class BaleClient(MessagesMethods, MediaMethods):
    def __init__(self, token: str, *, timeout: float = 30.0):
        self.token = token
        self.base_url = f"https://tapi.bale.ai/bot{token}/"
        self._timeout = timeout
        self._handlers: list[Tuple[Any, Callable[[Message], Awaitable[None]]]] = []
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> "BaleClient":
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
        self._session = None

    async def _ensure_session(self) -> None:
        if not self._session or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self._timeout)
            self._session = aiohttp.ClientSession(timeout=timeout)

    async def _request(self, method: str, data: Any = None, is_multipart: bool = False) -> Any:
        await self._ensure_session()
        assert self._session is not None

        url = self.base_url + method

        try:
            if is_multipart:
                async with self._session.post(url, data=data) as response:
                    return await response.json()

            async with self._session.post(url, json=data) as response:
                return await response.json()

        except (aiohttp.ClientError, asyncio.TimeoutError):
            raise

    def on(self, event_builder):
        def decorator(callback):
            self._handlers.append((event_builder, callback))
            return callback
        return decorator

    async def _run_handler(self, callback: Callable[[Message], Awaitable[None]], event: Message) -> None:
        try:
            await callback(event)
        except Exception:
            print(f"\n❌ Error in handler '{callback.__name__}':")
            traceback.print_exc()

    async def _poll(self):
        offset = 0
        print("BaleClient polling started")
        try:
            while True:
                try:
                    payload = {
                        "offset": offset,
                        "timeout": 10
                    }
                    response = await self._request("getUpdates", payload)

                    if response and response.get("ok"):
                        for update in response["result"]:
                            offset = update["update_id"] + 1
                            await self._process_update(update)

                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    print(f"Network Warning: {e}. Retrying in 3 second...")
                    await asyncio.sleep(3)

                except Exception as e:
                    print(f"Error: {e}. Retrying in 3 second...")
                    await asyncio.sleep(1)

                await asyncio.sleep(0.1)

        except asyncio.CancelledError:
            pass
        finally:
            await self.close()

    async def _process_update(self, update):
        for event_builder, callback in self._handlers:
            if isinstance(event_builder, NewMessage) and "message" in update:
                event = Message(client=self, data=update["message"])

                if event_builder.filter(event):
                    asyncio.create_task(self._run_handler(callback, event))
            
            elif isinstance(event_builder, CallbackQuery) and "callback_query" in update:
                event = CallbackQueryEvent(client=self, data=update["callback_query"])

                if event_builder.filter(event):
                    asyncio.create_task(self._run_handler(callback, event))

    def run_until_disconnected(self):
        try:
            asyncio.run(self._poll())
        except RuntimeError:
            return asyncio.create_task(self._poll())
        except KeyboardInterrupt:
            print("Bot stopped successfully.")