class BaleObject:
    
    def __repr__(self) -> str:
        attributes = []
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                attributes.append(f"{key}={value}")
            
        return f"<{self.__class__.__name__} {', '.join(attributes)}>"

    def __str__(self) -> str:
        return self.__repr__()