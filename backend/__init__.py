import dataclasses
import os

import dotenv

from .utils import parse_bool


@dataclasses.dataclass
class Settings:
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


_env = dotenv.dotenv_values("env")


def _interpolate(f: dataclasses.Field) -> bool | int | str:
    e_val: str | None = os.environ.get(f.name)
    d_val: str | None = _env.get(f.name)
    val = e_val or d_val
    if f.type == bool:
        return parse_bool(val, f.default)
    if f.type == int:
        return int(val) if val is not None else f.default
    return val if val is not None else f.default


settings = Settings(
    **{
        k.name: _interpolate(k)
        for k in dataclasses.fields(Settings)
    }  # fmt: skip
)


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
