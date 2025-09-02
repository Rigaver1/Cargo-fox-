import re
from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


class Platform(str, Enum):
    """Supported messenger platforms."""

    TELEGRAM = "telegram_desktop"
    WHATSAPP = "whatsapp_business"
    WECHAT = "wechat_work"


# Simulated in-memory storage; in real code these would be DB calls
USERS: Dict[tuple, Dict[str, Any]] = {
    ("123", Platform.TELEGRAM): {"user_id": 1, "name": "Alice"},
    ("456", Platform.WHATSAPP): {"user_id": 2, "name": "Bob"},
    ("789", Platform.WECHAT): {"user_id": 3, "name": "Chen"},
}

APPLICATIONS: List[Dict[str, Any]] = []
COMMUNICATION_HISTORY: Dict[int, List[str]] = {}


@dataclass
class Application:
    """Represents an application created from a forwarded message."""

    id: int
    link: str
    user_id: int


def identify_sender(sender_id: str, platform: Platform) -> Dict[str, Any]:
    """Return internal representation for a user on a specific platform.

    Raises:
        ValueError: if the sender is unknown for the platform.
    """

    key = (sender_id, platform)
    if key not in USERS:
        raise ValueError(f"Unknown sender {sender_id} on platform {platform}")
    return USERS[key]


def parse_1688_link(text: str) -> Optional[str]:
    """Extract 1688 link from text if present."""

    match = re.search(r"https?://[^\s]*1688\.com/\S*", text)
    return match.group(0) if match else None


def create_application(link: str, sender_info: Dict[str, Any]) -> Application:
    """Create a new application linked to the sender."""

    app = Application(id=len(APPLICATIONS) + 1, link=link, user_id=sender_info["user_id"])
    APPLICATIONS.append(app.__dict__)
    return app


def handle_forwarded_message(text: str, sender_id: str, platform: Platform) -> Optional[Application]:
    """Process a forwarded message and create an application if it contains a 1688 link."""

    sender_info = identify_sender(sender_id, platform)
    link = parse_1688_link(text)
    if not link:
        return None

    application = create_application(link, sender_info)
    COMMUNICATION_HISTORY.setdefault(sender_info["user_id"], []).append(text)
    return application


class TelegramClient:
    """Placeholder Telegram Desktop API client."""

    def send_message(self, chat_id: str, text: str) -> None:  # pragma: no cover - placeholder
        print(f"Telegram message to {chat_id}: {text}")

    def fetch_history(self, chat_id: str) -> List[str]:  # pragma: no cover - placeholder
        return COMMUNICATION_HISTORY.get(int(chat_id), [])


class WhatsAppClient:
    """Placeholder WhatsApp Business API client."""

    def send_message(self, chat_id: str, text: str) -> None:  # pragma: no cover - placeholder
        print(f"WhatsApp message to {chat_id}: {text}")

    def fetch_history(self, chat_id: str) -> List[str]:  # pragma: no cover - placeholder
        return COMMUNICATION_HISTORY.get(int(chat_id), [])


class WeChatClient:
    """Placeholder WeChat Work API client with status support."""

    def send_message(self, chat_id: str, text: str) -> None:  # pragma: no cover - placeholder
        print(f"WeChat message to {chat_id}: {text}")

    def fetch_history(self, chat_id: str) -> List[str]:  # pragma: no cover - placeholder
        return COMMUNICATION_HISTORY.get(int(chat_id), [])

    def get_status(self, user_id: str) -> str:  # pragma: no cover - placeholder
        return "online" if int(user_id) % 2 else "offline"


def fetch_related_data(user_id: int) -> Dict[str, Any]:
    """Instantly load active applications and communication history for a user."""

    active_apps = [app for app in APPLICATIONS if app["user_id"] == user_id]
    history = COMMUNICATION_HISTORY.get(user_id, [])
    return {"active_applications": active_apps, "communication_history": history}

