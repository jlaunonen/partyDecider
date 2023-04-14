import typing

from fastapi import Depends, HTTPException, Request

from .db import AsyncSession, request_database


async def require_admin(request: Request):
    if request.client.host != "127.0.0.1":
        raise HTTPException(status_code=401, detail="Access denied")


Database = typing.Annotated[AsyncSession, Depends(request_database)]
