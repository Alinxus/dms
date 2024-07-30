from dataclasses import dataclass

@dataclass
class Message:
    platform: str
    recipient: str
    message: str