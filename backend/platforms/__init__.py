import sys


class PlatformBase:
    @classmethod
    def spawn_browser(cls, cmdline: str | None, admin_url: str):
        raise NotImplementedError

    @classmethod
    def get_hostname(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_ips(cls) -> list[str]:
        raise NotImplementedError


if sys.platform.startswith("linux"):
    from .linux import Platform
elif sys.platform.startswith("darwin"):
    from .mac import Platform
else:
    from .windows import Platform
