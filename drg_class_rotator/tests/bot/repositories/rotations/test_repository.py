import json
from typing import List
from unittest.mock import AsyncMock

import pytest
from pydantic import parse_raw_as

from bot.models import Dwarf, DwarfClasses
from bot.repositories.rotations.repository import RotationRepository
from config import settings
from tests.bot.repositories.rotations.mocks import (
    redis_value_without_previous_class,
    redis_value_with_previous_class,
)


class TestRotationRepository:
    def setup_class(self):
        self.repository = RotationRepository()
        self.repository.redis = AsyncMock()

    def setup_method(self):
        self.repository.redis.reset_mock(return_value=True, side_effect=True)

    def test_create_key(self):
        discord_guild_id = discord_user_id = 1
        key = self.repository._create_key(discord_guild_id=discord_guild_id, discord_user_id=discord_user_id)

        assert key == f'{discord_guild_id}-{discord_user_id}'

    @pytest.mark.asyncio
    @pytest.mark.parametrize('redis_value',
                             [redis_value_without_previous_class, redis_value_with_previous_class])
    async def test_get_user_rotation(self, redis_value):
        self.repository.redis.get.return_value = redis_value

        discord_guild_id = discord_user_id = 1
        value = await self.repository.get_user_rotation(
            discord_guild_id=discord_guild_id,
            discord_user_id=discord_user_id
        )

        key = self.repository._create_key(discord_guild_id, discord_user_id)
        self.repository.redis.get.assert_called_once_with(name=key)

        parsed_mock = parse_raw_as(List[Dwarf], redis_value)
        assert value == parsed_mock

    @pytest.mark.asyncio
    async def test_get_user_rotation_rotation_not_exist(self):
        self.repository.redis.get.return_value = None

        discord_guild_id = discord_user_id = 1
        value = await self.repository.get_user_rotation(
            discord_guild_id=discord_guild_id,
            discord_user_id=discord_user_id
        )

        assert value == []

    @pytest.mark.asyncio
    async def test_set_user_rotation(self):
        discord_guild_id = discord_user_id = 1
        dwarves = [Dwarf(current_class=DwarfClasses.SCOUT), Dwarf(current_class=DwarfClasses.GUNNER)]

        await self.repository.set_user_rotation(
            discord_guild_id=discord_guild_id,
            discord_user_id=discord_user_id,
            dwarves=dwarves
        )

        key = self.repository._create_key(discord_guild_id, discord_user_id)
        self.repository.redis.set.assert_called_once_with(
            name=key,
            value=json.dumps([dwarf.dict() for dwarf in dwarves]),
            ex=settings.REDIS_ROTATION_LIFETIME
        )
