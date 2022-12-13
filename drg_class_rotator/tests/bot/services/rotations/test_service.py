from unittest.mock import create_autospec

import pytest

from bot.repositories.rotations.repository import RotationRepository
from bot.services.rotations import exceptions
from bot.services.rotations.service import RotationService
from tests.bot.services.rotations.mocks import dwarves_with_previous_class, dwarves_without_previous_class


class TestRotationService:
    def setup_class(self):
        self.service = RotationService()
        self.service._repository = create_autospec(RotationRepository)

    def setup_method(self):
        self.service._repository.reset_mock(return_value=True, side_effect=True)

    @pytest.mark.parametrize('player_count', [1, 2, 3, 4])
    @pytest.mark.parametrize('unique_classes', [False, True])
    def test_generate_random_rotation(self, player_count, unique_classes):
        rotation_image = self.service.generate_random_rotation(player_count=player_count, unique_classes=unique_classes)

        assert isinstance(rotation_image, bytes)

    @pytest.mark.parametrize('player_count', [5])
    @pytest.mark.parametrize('unique_classes', [False, True])
    def test_generate_random_rotation_incorrect_player_count(self, player_count, unique_classes):
        with pytest.raises(exceptions.IncorrectPlayerCountError):
            self.service.generate_random_rotation(player_count=player_count, unique_classes=unique_classes)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('player_count', [1, 2, 3, 4])
    async def test_generate_rotation_based_on_previous_classes(self, player_count):
        discord_guild_id = discord_user_id = 1
        rotation_image = await self.service.generate_rotation_based_on_previous_classes(
            player_count=player_count,
            discord_guild_id=discord_guild_id,
            discord_user_id=discord_user_id
        )

        self.service._repository.set_user_rotation.assert_called_once()

        assert isinstance(rotation_image, bytes)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('player_count', [5])
    async def test_generate_rotation_based_on_previous_classes_incorrect_player_count(self, player_count):
        discord_guild_id = discord_user_id = 1
        with pytest.raises(exceptions.IncorrectPlayerCountError):
            await self.service.generate_rotation_based_on_previous_classes(
                player_count=player_count,
                discord_guild_id=discord_guild_id,
                discord_user_id=discord_user_id
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize('repository_response', [dwarves_without_previous_class, dwarves_with_previous_class])
    async def test_generate_next_rotation_based_on_previous_classes(self, repository_response):
        self.service._repository.get_user_rotation.return_value = repository_response

        discord_guild_id = discord_user_id = 1
        rotation_image = await self.service.generate_next_rotation_based_on_previous_classes(
            discord_guild_id=discord_guild_id,
            discord_user_id=discord_user_id
        )

        self.service._repository.get_user_rotation.assert_called_once_with(
            discord_guild_id=discord_guild_id,
            discord_user_id=discord_user_id
        )
        self.service._repository.set_user_rotation.assert_called_once()

        assert isinstance(rotation_image, bytes)

    @pytest.mark.asyncio
    async def test_generate_rotation_based_on_previous_classes_user_rotation_not_found(self):
        self.service._repository.get_user_rotation.return_value = []

        discord_guild_id = discord_user_id = 1
        with pytest.raises(exceptions.UserRotationNotFoundError):
            await self.service.generate_next_rotation_based_on_previous_classes(
                discord_guild_id=discord_guild_id,
                discord_user_id=discord_user_id
            )

        self.service._repository.get_user_rotation.assert_called_once_with(
            discord_guild_id=discord_guild_id,
            discord_user_id=discord_user_id
        )
