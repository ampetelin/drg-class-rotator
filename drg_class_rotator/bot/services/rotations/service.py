from bot.class_image_builder.builder import ClassImageBuilder
from bot.class_rotator import exceptions as cr_exceptions
from bot.class_rotator.rotations import random_rotation, rotation_based_on_previous_classes
from bot.repositories.rotations import RotationRepository
from bot.services.rotations.exceptions import IncorrectPlayerCountError, UserRotationNotFoundError


class RotationService:
    def __init__(self):
        self._repository = RotationRepository()
        self._image_builder = ClassImageBuilder()

    def generate_random_rotation(self, player_count: int, unique_classes: bool) -> bytes:
        """
        Генерирует случайную ротацию и получает её изображение

        Args:
            player_count: количество игроков в ротации
            unique_classes: признак уникальности классов дворфов

        Returns:
            Изображение ротации
        """
        try:
            dwarves = random_rotation(player_count=player_count, unique_classes=unique_classes)
        except cr_exceptions.IncorrectCountError as ex:
            raise IncorrectPlayerCountError(ex)

        dwarf_classes = [dwarf.current_class for dwarf in dwarves]
        rotation_image = self._image_builder.get_image_of_classes(dwarf_classes=dwarf_classes)

        return rotation_image

    async def generate_rotation_based_on_previous_classes(self,
                                                          player_count: int,
                                                          discord_guild_id: int,
                                                          discord_user_id: int) -> bytes:
        """
        Генерирует первоначальную ротацию, основанную на предыдущих классах и получает её изображение

        Args:
            player_count: количество игроков в ротации
            discord_guild_id: идентификатор гильдии Discord
            discord_user_id: идентификатор пользователя Discord

        Raises:
            IncorrectPlayerCountError: возбуждаемое исключение в случае указания количества игроков в недопустимом
                диапазоне

        Returns:
            Изображение ротации
        """
        try:
            dwarves = random_rotation(player_count=player_count, unique_classes=True)
        except cr_exceptions.IncorrectCountError as ex:
            raise IncorrectPlayerCountError(ex)

        await self._repository.set_user_rotation(
            discord_guild_id=discord_guild_id,
            discord_user_id=discord_user_id,
            dwarves=dwarves
        )

        dwarf_classes = [dwarf.current_class for dwarf in dwarves]
        rotation_image = self._image_builder.get_image_of_classes(dwarf_classes=dwarf_classes)

        return rotation_image

    async def generate_next_rotation_based_on_previous_classes(self,
                                                               discord_guild_id: int,
                                                               discord_user_id: int) -> bytes:
        """
        Генерирует следующую ротацию, основанную на предыдущих класса и получает её изображение

        Args:
            discord_guild_id: идентификатор гильдии Discord
            discord_user_id: идентификатор пользователя Discord

        Raises:
            UserRotationNotFoundError: возбуждаемое исключение в случае отсутствия сохраненной ротации пользователя

        Returns:
            Изображение ротации
        """
        dwarves = await self._repository.get_user_rotation(
            discord_guild_id=discord_guild_id,
            discord_user_id=discord_user_id
        )
        if not dwarves:
            raise UserRotationNotFoundError('User rotations was not found. It is necessary to generate a new rotations')

        dwarves = rotation_based_on_previous_classes(dwarves=dwarves)
        await self._repository.set_user_rotation(
            discord_guild_id=discord_guild_id,
            discord_user_id=discord_user_id,
            dwarves=dwarves
        )

        dwarf_classes = [dwarf.current_class for dwarf in dwarves]
        rotation_image = self._image_builder.get_image_of_classes(dwarf_classes=dwarf_classes)

        return rotation_image
