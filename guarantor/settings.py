import enum
from pathlib import Path
from tempfile import gettempdir
from typing import Dict

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
    main_wallet_config: Dict[str, str] = {}
    tron_trx_commission: int = 28_000_000

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

    """
    @property
    def main_wallet_config(self) -> Dict[str, str]:
        file_path = os.path.join(os.path.dirname(__file__), 'main_wallet.json')
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                self._main_wallet_config = json.loads(f.read())
        else:
            client = Tron(network=self.tron_network)
            self._main_wallet_config = client.generate_address()
            with open(file_path, 'w') as f:
                json.dump(self._main_wallet_config, f)

        return self._main_wallet_config
    """

    class Config:
        env_file = ".env"
        env_prefix = "GUARANTOR_"
        env_file_encoding = "utf-8"


settings = Settings()
