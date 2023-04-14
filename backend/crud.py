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
