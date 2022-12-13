from io import BytesIO

from discord import Interaction, app_commands, File
from discord.ext import commands

from bot.services.rotations import exceptions
from bot.services.rotations.service import RotationService


class RotateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._rotation_service = RotationService()
        self._rotation_filename = 'rotations.png'

    @app_commands.command(description='Генерирует случайную ротацию дворфов')
    @app_commands.describe(
        players='Количество игроков',
        unique='Признак уникальности классов игроков'
    )
    async def random(self, interaction: Interaction, players: int, unique: bool = False):
        rotation_image = self._rotation_service.generate_random_rotation(
            player_count=players,
            unique_classes=unique
        )

        await interaction.response.send_message(file=File(fp=BytesIO(rotation_image), filename=self._rotation_filename))

    @app_commands.command(description='Генерирует ротацию дворфов с учетом предыдущих классов')
    @app_commands.describe(
        players='Количество игроков',
    )
    async def rotation(self,
                       interaction: Interaction,
                       players: int):
        try:
            rotation_image = await self._rotation_service.generate_rotation_based_on_previous_classes(
                player_count=players,
                discord_guild_id=interaction.guild_id,
                discord_user_id=interaction.user.id
            )
        except exceptions.IncorrectPlayerCountError:
            return await interaction.response.send_message(
                'Указано недопустимое количество игроков. Допустимые значения: 1-4'
            )

        await interaction.response.send_message(file=File(fp=BytesIO(rotation_image), filename=self._rotation_filename))

    @app_commands.command(description='Генерирует следующую ротацию дворфов, основанную на предыдущей ротации')
    async def rotate(self, interaction: Interaction):
        try:
            rotation_image = await self._rotation_service.generate_next_rotation_based_on_previous_classes(
                discord_guild_id=interaction.guild_id,
                discord_user_id=interaction.user.id
            )
        except exceptions.UserRotationNotFoundError:
            msg = "Отсутствует предыдущая ротация. Пожалуйста, сгенерируйте новую ротацию. " \
                  "(Напр.: `/rotations players:4`)"
            return await interaction.response.send_message(msg)

        await interaction.response.send_message(file=File(fp=BytesIO(rotation_image), filename=self._rotation_filename))


async def setup(bot):
    await bot.add_cog(RotateCog(bot))
