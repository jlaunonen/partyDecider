import json
import os
import subprocess
import threading
from functools import cache

from . import PlatformBase


class Platform(PlatformBase):
    @classmethod
    def spawn_browser(cls, cmdline: str | None, admin_url: str):
        command = cmdline or "xdg-open {admin}"
        cmd = command.format(admin=admin_url)
        if not cmd:
            return

        # We don't want to wait for the launch to exit, so we do that in a thread.
        # That way the xdg-open (or whatever) can freely either complete immediately, or
        # block the call (of which we detach after timeout).
        def runner():
            proc = subprocess.Popen(cmd, shell=True)
            try:
                proc.communicate(timeout=5)
                print("Browser launch finished, returned {}".format(proc.returncode))
            except subprocess.TimeoutExpired:
                print("Browser launch moved to back, on PID {}".format(proc.pid))

        threading.Thread(target=runner, name="browserLauncher").start()

    @classmethod
    @cache
    def get_hostname(cls) -> str:
        return (
            os.environ.get("HOSTNAME")
            or subprocess.check_output("hostname").decode().strip()
        )

    @classmethod
    @cache
    def get_ips(cls) -> list[str]:
        try:
            ip_doc = json.loads(
                subprocess.check_output(["ip", "-j", "addr", "show", "up"]).decode()
            )
        except subprocess.SubprocessError:
            return []

        # Find addresses from `[].addr_info[].local` for items having operstate value "UP"
        ips: list[str] = []
        for ip_info in ip_doc:
            if ip_info.get("operstate", "DOWN") != "UP":
                continue
            for addr_info in ip_info.get("addr_info", []):
                addr = addr_info.get("local")
                if addr:
                    if addr_info.get("family") == "inet6":
                        ips.append("[%s]" % addr)
                    else:
                        ips.append(addr)

        return ips

    @classmethod
    def get_steam_root(cls) -> str | None:
        for path in (".steam", ".steam/steam", ".steam/root", ".local/share/Steam"):
            if (
                os.path.isdir(path)
                and os.path.isdir(path + "/config")
                and os.path.isdir(path + "/appcache")
            ):
                return path
