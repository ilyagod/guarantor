import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic import BaseSettings
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "guarantor"
    db_pass: str = "guarantor"
    db_base: str = "guarantor"
    db_echo: bool = False

    kafka_bootstrap_servers: list[str] = ["guarantor-kafka:9092"]

    tron_network: str = "shasta"

    disable_check_payments: bool = True
    tron_main_wallet: str = ""
    usdt_trc20_address: str = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    tron_fee_limit: float = 5_000_000

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgres",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    class Config:
        env_file = ".env"
        env_prefix = "GUARANTOR_"
        env_file_encoding = "utf-8"


settings = Settings()
