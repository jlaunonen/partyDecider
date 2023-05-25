import os
import signal
from typing import Annotated

import anyio
from fastapi import APIRouter, Body, Depends, HTTPException, Query

from . import crud, schemas
from .dependencies import Database, require_admin
from .state import State
from .vdf.game_gatherer import main as game_gatherer


router = APIRouter(
    dependencies=[Depends(require_admin)],
    responses={
        401: {"description": "Unauthorized"},
    },
    tags=["admin"],
)


@router.get(
    "/all",
    summary="Get all apps/games",
)
async def get_all(db: Database) -> list[schemas.App]:
    apps = crud.get_apps(db)
    return apps


@router.get(
    "/enabled",
    summary="Get enabled apps/games",
)
async def get_enabled(db: Database) -> list[schemas.App]:
    apps = crud.get_apps(db, lambda app: app.enabled)
    return apps


@router.post(
    "/enabled",
    summary="Set enabled apps/games",
)
async def set_enabled(
    db: Database,
    items: Annotated[list[int], Body()],
    by_steam_id: Annotated[bool, Query()] = False,
) -> schemas.Message:
    """List of ID's (or Steam-ID's if by_steam_id is true) that should be enabled for voting."""
    try:
        if by_steam_id:
            crud.set_enabled_by_steam_id(db, items)
        else:
            crud.set_enabled(db, items)
    except KeyError as e:
        raise HTTPException(422, detail=e.args[0])
    return schemas.Message.ok()


@router.post(
    "/rescan",
    summary="Rescan all installed apps/games",
)
async def rescan_games(db: Database) -> int:
    games = await anyio.to_thread.run_sync(game_gatherer, lambda a, b: None)
    return crud.set_apps(db, games)


@router.get(
    "/shutdown",
    summary="Shutdown the server application",
)
async def shutdown() -> schemas.Message:
    # Expect X_SERV_PID is set in __main__.
    s_pid = os.environ.get("X_SERV_PID")
    if s_pid is not None:
        os.kill(int(s_pid), signal.SIGINT)
    else:
        import sys

        print("X_SERV_PID not found!?", file=sys.stderr)
        # Hope that there is no parent supervisor process.
        signal.raise_signal(signal.SIGINT)
    return schemas.Message.ok()


@router.post(
    "/voting",
)
async def add_voting_session(
    db: Database, state: State, parameters: Annotated[schemas.NewVotingSession, Body()]
) -> schemas.VotingSession:
    apps = crud.get_apps(db, lambda app: app.enabled)
    return schemas.VotingSession.from_orm(state.voting_sessions.new_session(apps, parameters))
