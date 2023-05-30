import dataclasses

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8192
    DB_PATH: str = "db.csv"
    NO_BROWSER: bool = False

    # Command line, %a is replaced with admin url.
    BROWSER_CMD: str | None = None

    # Command to start frontend Vite dev server when outside zipapp.
    # %h will be replaced with HOST, %p will be replaced with VITE_DEV_PORT.
    VITE_DEV_CMD: str | None = "npm run dev -- --host %h --port %p"
    VITE_DEV_PORT: int = 8193

    # Path to steam config root. The directory should contain both appcache and config subdirectories.
    # If not set, Platform.get_steam_root() is used to detect it.
    STEAM_CONFIG_ROOT: str | None = None

    class Config:
        env_file = ["env", "env.txt"]


settings = Settings()


def get_steam_config_root():
    from .platforms import Platform

    if settings.STEAM_CONFIG_ROOT is not None:
        return settings.STEAM_CONFIG_ROOT
    else:
        return Platform.get_steam_root()


@dataclasses.dataclass()
class RuntimeConfig:
    CLIENT_URL: str = dataclasses.field(init=False)
    ADMIN_URL: str = dataclasses.field(init=False)
    STEAM_CONFIG_ROOT: str = dataclasses.field(default_factory=get_steam_config_root)

    IS_ZIP_APP: bool = False

    VITE_DEV_URL: str | None = f"http://{settings.HOST}:{settings.VITE_DEV_PORT}"


config = RuntimeConfig()
