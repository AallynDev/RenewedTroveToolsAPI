from beanie import Document, Indexed
from pydantic import Field

from string import ascii_letters, digits
from random import choices

from datetime import datetime
from typing import Optional


def generate_id():
    return "".join(choices(ascii_letters + digits, k=32))


class User(Document):
    discord_id: int = Indexed(int, unique=True)
    internal_token: str = Field(default_factory=generate_id)
    created_at: datetime
    updated_at: datetime
    last_login: datetime
    username: Optional[str] = None
    name: Optional[str] = None
    avatar_hash: Optional[str] = None
    premium_ends: Optional[datetime] = None
    is_premium: bool = False
    is_banned: bool = False
    is_admin: bool = False

    @property
    def mod_profiles_limit(self):
        return 12 if self.is_premium else 3

    @property
    def avatar_url(self):
        if self.has_avatar is False:
            return self.default_avatar
        if self.discord_id < 10000000:
            if self.avatar_hash.startswith("//"):
                return f"https:{self.avatar_hash}"
            else:
                return f"https://trovesaurus.com/data/catalog/{self.avatar_hash}.png"
        if self.avatar_hash.startswith("a_"):
            return f"https://cdn.discordapp.com/avatars/{self.discord_id}/{self.avatar_hash}.gif"
        return f"https://cdn.discordapp.com/avatars/{self.discord_id}/{self.avatar_hash}.png"

    @property
    def has_avatar(self):
        return self.avatar_hash is not None

    @property
    def default_avatar(self):
        index = str((self.discord_id >> 22) % 6)
        return f"https://cdn.discordapp.com/embed/avatars/{index}.png"

    @property
    def reset_url(self):
        return f"https://kiwiapi.slynx.xyz/v1/user/discord/reset_token?token={self.internal_token}"

    def reset_token(self):
        self.internal_token = generate_id()
        return self.internal_token
