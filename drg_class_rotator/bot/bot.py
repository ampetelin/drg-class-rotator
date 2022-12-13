import logging

from discord import Intents
from discord.ext import commands

cog_extensions = (
    'bot.cogs.rotations',
)

logger = logging.getLogger(__name__)


class DRGClassRotatorBot(commands.Bot):
    async def setup_hook(self):
        logger.info('Loading cog extensions...')
        await self.load_extensions()
        logger.info('loading cog extensions completed successfully')

        logger.info('CommandTree Synchronization...')
        sync_command = await self.tree.sync()
        logger.info(f'CommandTree synchronization completed successfully: {[command.name for command in sync_command]}')

    async def load_extensions(self):
        for cog in cog_extensions:
            logger.debug(f'Loading {cog} cog extensions')
            await self.load_extension(cog)
            logger.debug(f'Cog extension {cog} loaded successfully')


intents = Intents.default()
intents.message_content = True

bot = DRGClassRotatorBot(command_prefix='/', intents=intents)
