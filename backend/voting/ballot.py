from __future__ import annotations

from ..pd_types import VoteTarget, Vote


class Ballot:
    LAST_PLACE = 9000

    @classmethod
    def create(cls, votes: dict[VoteTarget, Vote]) -> Ballot:
        if votes and max(votes.values()) >= cls.LAST_PLACE:
            raise ValueError("Invalid vote")

        return cls(votes)

    def __init__(self, votes: dict[VoteTarget, Vote]):
        self.votes = votes

    def get_vote(self, target: VoteTarget):
        vote = self.votes.get(target)
        if vote is None or vote < 1:
            return self.LAST_PLACE
        return vote

    def __repr__(self):
        return f"Ballot({self.votes!r})"
