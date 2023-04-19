from typing import Callable

from . import models, schemas
from .db import AsyncSession


def get_apps(
    session: AsyncSession, flt: Callable[[models.AppItem], bool] = lambda _: True
) -> list[schemas.App]:
    return list(
        schemas.App(
            id=app.id,
            steam_id=app.steam_id,
            name=app.name,
        )
        for app in session.db.apps.values()
        if flt(app)
    )


def set_enabled(session: AsyncSession, ids: list[int]):
    app_ids = set(a.id for a in session.db.apps.values())
    for _id in ids:
        if _id not in app_ids:
            raise KeyError("App id {} does not exist".format(_id))
    id_set = set(ids)
    for app in session.db.apps.values():
        app.enabled = app.id in id_set


def set_enabled_by_steam_id(session: AsyncSession, ids: list[int]):
    app_ids = set(a.steam_id for a in session.db.apps.values())
    for _id in ids:
        if _id not in app_ids:
            raise KeyError("Steam id {} does not exist".format(_id))
    id_set = set(ids)
    for app in session.db.apps.values():
        app.enabled = app.steam_id in id_set


def set_apps(session: AsyncSession, games: list[dict[str, str | int]]) -> int:
    new_apps: dict[int, models.AppItem] = {}
    for index, game in enumerate(games, start=1):
        new_apps[index] = models.AppItem(
            id=index,
            steam_id=game["appid"],
            name=game["name"],
            enabled=True,  # TODO: Remove non-default
        )

    session.db.apps = new_apps
    return len(new_apps)
