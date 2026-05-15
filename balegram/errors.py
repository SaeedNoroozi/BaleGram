from typing import Optional


class BaleGramError(Exception):
    def __init__(self, message: str, error_code: Optional[int] = None):
        self.message = message
        self.error_code = error_code

        prefix = f"[{error_code}] " if error_code else ""
        super().__init__(f"{prefix}{message}")


class BadRequestError(BaleGramError):
    pass  # 400


class UnauthorizedError(BaleGramError):
    pass  # 401


class ForbiddenError(BaleGramError):
    pass  # 403


class ConflictError(BaleGramError):
    pass  # 409


class RateLimitError(BaleGramError):
    pass  # 429


class ServerError(BaleGramError):
    pass  # 500

class ChatNotFoundError(BadRequestError): pass
class InvalidTokenError(UnauthorizedError): pass
class MessageNotModifiedError(BadRequestError): pass

class FileError(BaleGramError):
    def __init__(self, message: str):
        super().__init__(message)

class FileTooLargeError(FileError):
    pass

class FileDownloadError(FileError):
    pass

class LocalFileSystemError(FileError):
    pass

def check_api_result(result: dict) -> None:
    if result.get("ok", True):
        return

    error_code = result.get("error_code")
    description = result.get("description", "Unknown error")
    description_lower = description.lower()

    if "chat not found" in description_lower or "no such group or user" in description_lower:
        raise ChatNotFoundError(description, error_code)
        
    if "message is not modified" in description_lower:
        raise MessageNotModifiedError(description, error_code)

    if error_code == 400:
        raise BadRequestError(description, error_code)

    elif error_code == 401:
        raise InvalidTokenError(description, error_code)

    elif error_code == 403:
        raise ForbiddenError(description, error_code)

    elif error_code == 409:
        raise ConflictError(description, error_code)

    elif error_code == 429:
        raise RateLimitError(description, error_code)

    elif error_code and error_code >= 500:
        raise ServerError(description, error_code)

    else:
        raise BaleGramError(description, error_code)
