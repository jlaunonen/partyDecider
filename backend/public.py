# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from . import crud, schemas, models
from .dependencies import ClientToken, Database, VoteSessionManager, VotingSession
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
async def get_voting_list(sessions: VoteSessionManager) -> list[schemas.VotingSession]:
    return [schemas.VotingSession.from_orm(e) for e in sessions]


@router.post(
    "/voting/{vote_session_key}",
    summary="Submit ballot for voting session.",
    responses={
        404: {"description": "Session with given key does not exist."},
        423: {"description": "Session voting time has ended."},
    },
)
async def submit_ballot(
    client_token: ClientToken,
    sessions: VoteSessionManager,
    vote_session_key: str,
    ballot: Annotated[schemas.Ballot, Body()],
) -> schemas.Message:
    session = sessions.get(vote_session_key)
    if session is None:
        raise HTTPException(status_code=404)
    try:
        model = Ballot.create(ballot.ballot, client_token=client_token)
        session.add_ballot(model)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_423_LOCKED)
    return schemas.Message.ok()


@router.get("/voting/{vote_session_key}", summary="Get voting session result.")
async def get_voting_result(
    client_token: ClientToken, session: VotingSession, db: Database
) -> schemas.VotingSessionResult:
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

    if session.closed:
        items = [
            make_item(
                score=score,
                tid=tid,
            )
            for score, targets in result
            for tid in targets
        ]
    else:
        items = None
    ballot = session.get_ballot(client_token)

    return schemas.VotingSessionResult(
        key=session.key,
        name=session.name,
        created_at=session.created_at,
        ends_at=session.ends_at,
        closed=session.closed,
        responses=session.responses,
        has_voted=ballot is not None,
        ballot=ballot,
        items=items,
    )
