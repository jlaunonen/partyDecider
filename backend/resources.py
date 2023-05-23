# -*- coding: utf-8 -*-
import os
import typing

from fastapi import APIRouter, Depends, Path, HTTPException, Request, Query
from fastapi.responses import FileResponse

from .dependencies import Database, is_admin
from . import config, crud, models


router = APIRouter(
    tags=["resources"],
)


async def get_app_info(
    request: Request,
    db: Database,
    app_id: typing.Annotated[int, Path()],
    as_admin: typing.Annotated[bool, Query()] = False,
) -> models.AppItem:
    # Only enabled apps should be accessible, unless they are requested by admin for admin page.
    app_info = crud.get_app_by_id(db, app_id)
    if (
        app_info is None
        or not app_info.enabled
        and not (as_admin and is_admin(request))
    ):
        raise HTTPException(status_code=404)

    return app_info


def fallback_static_image(name: str):
    path = os.path.join("backend", "static", name)
    from .main import static_server
    if static_server is not None:
        return static_server.get_local_response(path)
    return FileResponse(path=path)


@router.get(
    "/icon/{app_id}",
    response_class=FileResponse,
    summary="App/game icon resource.",
)
async def res_icon(
    app_info: typing.Annotated[models.AppItem, Depends(get_app_info)],
) -> FileResponse:
    if app_info.steam_id is not None:
        filename = os.path.join(
            config.STEAM_CONFIG_ROOT,
            "appcache",
            "librarycache",
            str(app_info.steam_id) + "_icon.jpg",
        )
        if os.path.isfile(filename):
            return FileResponse(path=filename)

    return fallback_static_image("empty_icon.png")


@router.get(
    "/logo/{app_id}",
    response_class=FileResponse,
    summary="App/game header/logo resource.",
)
async def res_header(
    app_info: typing.Annotated[models.AppItem, Depends(get_app_info)],
) -> FileResponse:
    if app_info.steam_id is not None:
        filename = os.path.join(
            config.STEAM_CONFIG_ROOT,
            "appcache",
            "librarycache",
            str(app_info.steam_id) + "_header.jpg",
        )
        if os.path.isfile(filename):
            return FileResponse(path=filename)

    return fallback_static_image("empty_icon.png")
