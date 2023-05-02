import winreg

from . import PlatformBase


def open_key_or_none(key, sub_key, **kwargs) -> winreg.HKEYType | None:
    try:
        return winreg.OpenKey(key, sub_key, **kwargs)
    except OSError:
        return None


class Platform(PlatformBase):
    REG_KEY = r"SOFTWARE\Valve\Steam"

    # TODO

    @classmethod
    def spawn_browser(cls, cmdline: str | None, admin_url: str):
        print("** Browser spawning support is not implemented **")

    @classmethod
    def get_hostname(cls) -> str:
        print("** Hostname resolution support is not implemented **")
        return "localhost"

    @classmethod
    def get_ips(cls) -> list[str]:
        print("** IP resolution support is not implemented **")
        return ["127.0.0.1"]

    @classmethod
    def get_steam_root(cls) -> str | None:
        hkey = open_key_or_none(
            winreg.HKEY_CURRENT_USER, cls.REG_KEY
        ) or open_key_or_none(winreg.HKEY_LOCAL_MACHINE, cls.REG_KEY)
        if hkey is None:
            return None
        with hkey as key:
            return winreg.QueryValue(key, "SteamPath")
