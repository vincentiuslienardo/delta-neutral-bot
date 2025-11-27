from pydantic_settings import BaseSettings, SettingsConfigDict
from x10.perpetual.configuration import MAINNET_CONFIG


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    API_URL: str = MAINNET_CONFIG.stream_url
    PAIR: str = "HYPE-USD"


settings = Settings()
