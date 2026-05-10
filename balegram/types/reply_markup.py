from typing import List, Optional, Union
from .base import BaleObject

class InlineKeyboardButton(BaleObject):
    def __init__(
        self,
        text: str,
        callback_data: Optional[str] = None,
        url: Optional[str] = None,
        copy_text: Optional[str] = None,
    ):
        self.text = text
        self.callback_data = callback_data
        self.url = url
        self.copy_text = copy_text

    def to_dict(self) -> dict:
        data = {"text": self.text}

        if self.callback_data is not None:
            data["callback_data"] = self.callback_data
        elif self.url is not None:
            data["url"] = self.url
        elif self.copy_text is not None:
            data["copy_text"] = {"text": str(self.copy_text)}

        return data

class InlineKeyboardMarkup(BaleObject):
    def __init__(self, inline_keyboard: List[List[InlineKeyboardButton]]):
        self.inline_keyboard = inline_keyboard

    def to_dict(self) -> dict:
        return {
            "inline_keyboard": [
                [button.to_dict() for button in row] for row in self.inline_keyboard
            ]
        }

class KeyboardButton(BaleObject):
    def __init__(
        self,
        text: str,
        request_contact: Optional[bool] = False,
        request_location: Optional[bool] = False,
    ):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
    
    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "request_contact": self.request_contact,
            "request_location": self.request_location,
        }

class ReplyKeyboardMarkup(BaleObject):
    def __init__(self, keyboard: List[List[KeyboardButton]]):
        self.keyboard = keyboard

    def to_dict(self) -> dict:
        return {
            "keyboard": [
                [button.to_dict() for button in row] for row in self.keyboard
            ]
        }
    
class ReplyKeyboardRemove(BaleObject):
    def __init__(self, remove_keyboard: bool = True):
        self.remove_keyboard = remove_keyboard
    
    def to_dict(self) -> dict:
        return {
            "remove_keyboard": self.remove_keyboard,
        }
        

class Button:
    @staticmethod
    def inline(text: str, data: Union[str, bytes, int]) -> InlineKeyboardButton:
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        return InlineKeyboardButton(text, callback_data=str(data))

    @staticmethod
    def url(text: str, url: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(text, url=url)

    @staticmethod
    def copy(text: str, copy_data: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(text, copy_text=copy_data)

    @staticmethod
    def text(text: str, request_contact: Optional[bool] = False, request_location: Optional[bool] = False) -> KeyboardButton:
        return KeyboardButton(text, request_contact, request_location)