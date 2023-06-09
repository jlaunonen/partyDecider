# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException

from . import crud, schemas, models
from .dependencies import Database
from .state import State
from .voting.ballot import Ballot


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
    "/voting",
    summary="Get currently active voting sessions.",
)
async def get_voting_list(state: State) -> list[schemas.VotingSession]:
    return [schemas.VotingSession.from_orm(e) for e in state.sessions]


@router.post(
    "/voting/{vote_session_key}",
    summary="Submit ballot for voting session.",
)
async def submit_ballot(
    state: State, vote_session_key: str, ballot: Annotated[schemas.Ballot, Body()]
) -> schemas.Message:
    session = state.sessions.get(vote_session_key)
    if session is None:
        raise HTTPException(status_code=404)
    session.ballots.append(Ballot.create(ballot.ballot))
    return schemas.Message.ok()


@router.get("/voting/{vote_session_key}", summary="Get voting session result.")
async def get_voting_result(
    state: State, db: Database, vote_session_key: str
) -> schemas.VotingSessionResult:
    session = state.sessions.get(vote_session_key)
    if session is None:
        raise HTTPException(status_code=404)
    result = session.get_result()
    apps: dict[int, models.AppItem] = {
        app.id: app for app in db.db.apps.values() if app.enabled
    }

    def make_item(score: int, tid: int):
        app = apps[tid]
        return schemas.VotingItem(
            id=tid,
            steam_id=app.steam_id,
            name=app.name,
            score=score,
        )

    return schemas.VotingSessionResult(
        key=session.key,
        ends_at=session.ends_at,
        name=session.name,
        items=[
            make_item(
                score=score,
                tid=tid,
            )
            for score, targets in result
            for tid in targets
        ],
    )
