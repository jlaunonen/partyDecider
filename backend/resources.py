# -*- coding: utf-8 -*-
import os
import typing

from fastapi import APIRouter, Path, HTTPException, Request, Query
from fastapi.responses import FileResponse

from .dependencies import Database, is_admin
from . import config, crud


router = APIRouter(
    tags=["resources"],
)


@router.get(
    "/icon/{app_id}",
    response_class=FileResponse,
    summary="App/game icon resource.",
)
async def res_icon(
    request: Request,
    db: Database,
    app_id: typing.Annotated[int, Path()],
    as_admin: typing.Annotated[bool, Query()] = False,
) -> FileResponse:
    filename = os.path.join(
        config.STEAM_CONFIG_ROOT, "appcache", "librarycache", str(app_id) + "_icon.jpg"
    )
    enabled_apps = {app.steam_id for app in crud.get_apps(db, lambda app: app.enabled)}

    # Only enabled apps should be accessible, unless they are requested by admin for admin page.
    if (app_id in enabled_apps or as_admin and is_admin(request)) and os.path.isfile(
        filename
    ):
        return FileResponse(path=filename)

    raise HTTPException(status_code=404)


@router.get(
    "/logo/{app_id}",
    response_class=FileResponse,
    summary="App/game header/logo resource.",
)
async def res_header(
    request: Request,
    db: Database,
    app_id: typing.Annotated[int, Path()],
    as_admin: typing.Annotated[bool, Query()] = False,
) -> FileResponse:
    filename = os.path.join(
        config.STEAM_CONFIG_ROOT,
        "appcache",
        "librarycache",
        str(app_id) + "_header.jpg",
    )
    enabled_apps = {app.steam_id for app in crud.get_apps(db, lambda app: app.enabled)}

    # Only enabled apps should be accessible, unless they are requested by admin for admin page.
    if (app_id in enabled_apps or as_admin and is_admin(request)) and os.path.isfile(
        filename
    ):
        return FileResponse(path=filename)

    raise HTTPException(status_code=404)
