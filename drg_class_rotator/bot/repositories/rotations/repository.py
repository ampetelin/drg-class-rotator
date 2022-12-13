import json
from typing import List

import aioredis
from pydantic import parse_raw_as

from bot.models import Dwarf
from config import settings


class RotationRepository:
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_DSN)
        self.rotation_lifetime = settings.REDIS_ROTATION_LIFETIME

    async def get_user_rotation(self, discord_guild_id: int, discord_user_id: int) -> List[Dwarf]:
        """
        Получает ротацию пользователя Discord в гильдии

        Args:
            discord_guild_id: идентификатор гильдии Discord
            discord_user_id: идентификатор пользователя Discord

        Returns:
            Список дворфов, входящих в ротацию
        """
        key = self._create_key(discord_guild_id=discord_guild_id, discord_user_id=discord_user_id)
        value = await self.redis.get(key=key)
        if not value:
            return []

        return parse_raw_as(List[Dwarf], value)

    async def set_user_rotation(self, discord_guild_id: int, discord_user_id: int, dwarves: List[Dwarf]):
        """
        Сохраняет ротацию пользователя Discord в гильдии

        Args:
            discord_guild_id: идентификатор гильдии Discord
            discord_user_id: идентификатор пользователя Discord
            dwarves: список дворфов, входящих в ротацию
        """
        value = [dwarf.dict() for dwarf in dwarves]
        key = self._create_key(discord_guild_id=discord_guild_id, discord_user_id=discord_user_id)
        await self.redis.set(name=key, value=json.dumps(value), ex=self.rotation_lifetime)

    @staticmethod
    def _create_key(discord_guild_id: int, discord_user_id: int):
        return f'{discord_guild_id}-{discord_user_id}'
