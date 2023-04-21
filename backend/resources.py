# -*- coding: utf-8 -*-
import os
import typing

from fastapi import APIRouter, Path, HTTPException
from fastapi.responses import FileResponse

from . import config


router = APIRouter(
    tags=["resources"],
)


@router.get(
    "/icon/{app_id}",
    response_class=FileResponse,
    summary="App/game icon resource.",
)
async def res_icon(app_id: typing.Annotated[int, Path()]) -> FileResponse:
    filename = os.path.join(
        config.STEAM_CONFIG_ROOT, "appcache", "librarycache", str(app_id) + "_icon.jpg"
    )
    if not os.path.isfile(filename):
        raise HTTPException(status_code=404)

    return FileResponse(path=filename)


@router.get(
    "/logo/{app_id}",
    response_class=FileResponse,
    summary="App/game header/logo resource.",
)
async def res_header(app_id: typing.Annotated[int, Path()]) -> FileResponse:
    filename = os.path.join(
        config.STEAM_CONFIG_ROOT,
        "appcache",
        "librarycache",
        str(app_id) + "_header.jpg",
    )
    if not os.path.isfile(filename):
        raise HTTPException(status_code=404)

    return FileResponse(path=filename)
