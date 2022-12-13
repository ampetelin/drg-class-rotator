import logging
from typing import Optional

import sentry_sdk
from pydantic import BaseSettings, AnyHttpUrl, RedisDsn


class Settings(BaseSettings):
    DISCORD_BOT_TOKEN: str
    LOG_LEVEL: str = 'INFO'
    REDIS_DSN: RedisDsn
    REDIS_ROTATION_LIFETIME: int
    SENTRY_DSN: Optional[AnyHttpUrl]

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()

logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s] - %(message)s', level=settings.LOG_LEVEL)

sentry_sdk.init(dsn=settings.SENTRY_DSN, traces_sample_rate=1.0)
