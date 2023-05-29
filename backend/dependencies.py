import typing

from fastapi import Depends, HTTPException, Request

from .db import AsyncSession, request_database
from . import state as _state


async def require_admin(request: Request):
    if request.client.host != "127.0.0.1":
        raise HTTPException(status_code=401, detail="Access denied")


def is_admin(request: Request):
    return request.client.host == "127.0.0.1"


Database = typing.Annotated[AsyncSession, Depends(request_database)]


async def get_ballot_store(state: _state.State) -> _state.SessionManager:
    return state.voting_sessions

VoteSessionManager = typing.Annotated[_state.SessionManager, Depends(get_ballot_store)]
