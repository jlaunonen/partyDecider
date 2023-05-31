# -*- coding: utf-8 -*-
import typing

from fastapi import Depends, HTTPException, Path, Request

from .db import AsyncSession, request_database
from . import state as _state
from .voting import session


async def require_admin(request: Request):
    if request.client.host != "127.0.0.1":
        raise HTTPException(status_code=401, detail="Access denied")


def is_admin(request: Request):
    return request.client.host == "127.0.0.1"


Database = typing.Annotated[AsyncSession, Depends(request_database)]


async def get_ballot_store(state: _state.State) -> _state.SessionManager:
    return state.voting_sessions


VoteSessionManager = typing.Annotated[_state.SessionManager, Depends(get_ballot_store)]


async def get_voting_session(
    sessions: VoteSessionManager, vote_session_key: typing.Annotated[str, Path()]
) -> session.VotingSession:
    s = sessions.get(vote_session_key)
    if s is None:
        raise HTTPException(status_code=404)
    return s


VotingSession = typing.Annotated[session.VotingSession, Depends(get_voting_session)]


async def get_client_token(request: Request) -> str:
    client_token = request.client.host
    return client_token


ClientToken = typing.Annotated[str, Depends(get_client_token)]
