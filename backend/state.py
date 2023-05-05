from __future__ import annotations

import contextlib
import dataclasses
import typing

from fastapi import Depends, Request

from . import config, settings
from .voting.session import SessionManager


@dataclasses.dataclass
class StateData:
    sessions: SessionManager = dataclasses.field(default_factory=SessionManager)


state_data = StateData()


async def state(_: Request):
    return state_data


State = typing.Annotated[StateData, Depends(state)]


@contextlib.asynccontextmanager
async def dev_lifecycle():
    use_pickle = settings.DEBUG and not config.IS_ZIP_APP
    state_file = "state.pickle"

    if use_pickle:
        global state_data
        import os
        import pickle

        if os.path.exists(state_file):
            print("Loading previous state from", state_file)
            try:
                with open(state_file, "rb") as f:
                    state_data = pickle.load(f)
            except Exception as e:
                print("Error loading state, will remove the file:", e)
                os.unlink(state_file)

    yield

    if use_pickle:
        import pickle

        with open(state_file, "wb") as f:
            pickle.dump(state_data, f)
