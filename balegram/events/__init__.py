import re

class NewMessage:
    def __init__(self, pattern=None, func=None, from_users=None):
        self.func = func
        self.pattern = pattern
        self.from_users = from_users

        if isinstance(self.pattern, str):
            self.pattern = re.compile(self.pattern)

    def filter(self, event):
        if self.from_users is not None:
            from_users_list = self.from_users if isinstance(self.from_users, list) else [self.from_users]
            if event.sender_id not in from_users_list:
                return False

        if self.pattern:
            match = self.pattern.search(event.raw_text)
            if not match:
                return False
            
            event.pattern_match = match

        if self.func:
            if not self.func(event):
                return False

        return True