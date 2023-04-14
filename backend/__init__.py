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


_env = dotenv.dotenv_values("env")


def _interpolate(f: dataclasses.Field) -> bool | int | str:
    e_val: str | None = os.environ.get(f.name)
    d_val: str | None = _env.get(f.name)
    val = e_val or d_val
    if f.type == bool:
        return parse_bool(val, f.default)
    if f.type == int:
        return int(val) if val is not None else f.default
    return val or f.default


settings = Settings(
    **{
        k.name: _interpolate(k)
        for k in dataclasses.fields(Settings)
    }  # fmt: skip
)


@dataclasses.dataclass(init=False)
class RuntimeConfig:
    CLIENT_URL: str
    ADMIN_URL: str

    IS_ZIP_APP: bool = False


config = RuntimeConfig()
