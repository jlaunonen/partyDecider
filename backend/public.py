# -*- coding: utf-8 -*-

from fastapi import APIRouter

from . import crud, schemas
from .dependencies import Database


router = APIRouter(
    tags=["public"],
)


@router.get(
    "/apps",
    summary="Get enabled apps/games.",
)
async def get_apps(db: Database) -> list[schemas.App]:
    apps = crud.get_apps(db, lambda app: app.enabled)
    return apps


@router.get(
    "/votings",
    summary="Get currently active voting sessions.",
)
async def get_votings(db: Database):
    pass


@router.post(
    "/votings",
    summary="Submit ballot for voting session.",
)
async def submit_ballot(db: Database):
    pass
