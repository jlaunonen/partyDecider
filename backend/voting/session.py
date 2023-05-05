from __future__ import annotations

import datetime
import typing
import uuid

from .. import schemas
from ..pd_types import VoteTarget, VotingResult
from .systems.simple import Simple
from ..models import AppItem
from .ballot import Ballot


class VotingSession:
    def __init__(
        self,
        end: int | None,
        name: str | None,
        options: list[AppItem],
        key: str | None = None,
    ):
        self.key = key or str(uuid.uuid4())
        self.ballots: list[Ballot] = []
        self.ends_at: int | None = end
        self.name: str | None = name
        self.closed: bool = False
        self.options: list[AppItem] = options

    def add_ballot(self, ballot: Ballot):
        if self.closed or (
            self.ends_at is not None
            and self.ends_at < datetime.datetime.now().timestamp()
        ):
            self.closed = True
            raise ValueError("Voting has ended")
        self.ballots.append(ballot)

    def get_result(self) -> VotingResult:
        calc = Simple(list(VoteTarget(a.id) for a in self.options))
        result = calc.iter_ballots(self.ballots)
        return result


class SessionManager:
    def __init__(self):
        self.sessions: dict[str, VotingSession] = {}
        self._add(
            VotingSession(None, "Test", [], key="test-uuid")
        )  # TODO: Remove default test session

    def _add(self, session: VotingSession) -> VotingSession:
        self.sessions[session.key] = session
        return session

    def new_session(
        self, apps: list[AppItem], data: schemas.NewVotingSession
    ) -> VotingSession:
        return self._add(
            VotingSession(
                end=int(datetime.datetime.now().timestamp() + data.duration)
                if data.duration
                else None,
                name=data.name,
                options=apps,
            )
        )

    def get(self, key: str) -> VotingSession | None:
        return self.sessions.get(key)

    def __iter__(self) -> typing.Iterator[VotingSession]:
        return iter(self.sessions.values())
