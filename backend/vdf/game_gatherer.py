# -*- coding: utf-8 -*-
import dataclasses
import os
import sys
import typing

from .vdfparser import VdfBinary, VdfText, parse, parse_text
from .. import config


@dataclasses.dataclass(init=False)
class GatherState:
    current_app_info: dict
    current_app_data: dict

    def __init__(self):
        self.current_app_data = {}
        self.current_app_info = {}

    def reset(self, new_info: dict):
        self.current_app_data = {}
        self.current_app_info = new_info

    def copy_to(self, target: dict):
        target[self.current_app_info["app_id"]] = self.current_app_data


def default_progress(i: int, end: str):
    print("\rReading appinfo...", i, end=end)
    sys.stdout.flush()


def main(progress: typing.Callable[[int, str], None]) -> list[dict[str, str | int]]:
    if not os.path.exists(config.STEAM_CONFIG_ROOT):
        raise ValueError(
            "Steam config directory does not exist: %s" % config.STEAM_CONFIG_ROOT
        )

    appinfo_vdf = os.path.join(config.STEAM_CONFIG_ROOT, "appcache", "appinfo.vdf")
    if not os.path.exists(appinfo_vdf):
        raise ValueError("Steam appinfo does not exist: %s" % appinfo_vdf)

    libraryfolders_vdf = os.path.join(
        config.STEAM_CONFIG_ROOT, "config", "libraryfolders.vdf"
    )
    if not os.path.exists(libraryfolders_vdf):
        raise ValueError(
            "Steam library folder information does not exist: %s" % libraryfolders_vdf
        )

    data = {}
    state = GatherState()

    def app_data_gatherer(k, e, path: list):
        if isinstance(e, dict) and path == []:
            # Start of app
            state.reset(e)

        if e == VdfBinary.OBJ_END and path == ["app"]:
            state.copy_to(data)
            size = len(data)
            if size % 5 == 0:
                progress(size, "")

        if (
            (k == "appid" and path == ["app", "appinfo"])
            or (k == "name" and path == ["app", "appinfo", "common"])
            or (k == "type" and path == ["app", "appinfo", "common"])
        ):
            state.current_app_data[k] = e

    progress(0, "")
    with open(appinfo_vdf, "rb") as f:
        parse(f, app_data_gatherer)
    progress(len(data), "\n")

    # Gather installed apps from all library folders and produce data entries for them.
    apps: list[dict[str, str | int]] = []

    def installed_gatherer(k: str, v: str | object, path: list[str]):
        if (
            v is not VdfText.OBJ_END
            and len(path) == 3
            and path[0] == "libraryfolders"
            and path[2] == "apps"
        ):
            # k == appid, v == probably installation size
            app_id = int(k)
            info = data.get(app_id)
            if info is not None and info["type"].lower() not in ("tool", "music"):
                apps.append(info)

    with open(libraryfolders_vdf, "rt") as f:
        parse_text(f, installed_gatherer)

    return apps


if __name__ == "__main__":
    games = main(default_progress)
    print("Found {} games".format(len(games)))
    import pprint

    pprint.pprint(games)
