import typing


VoteTarget = typing.NewType("VoteTarget", int)
Vote = typing.NewType("Vote", int)

# List of tuples having score:int and targets with that score.
VotingResult = list[tuple[int, tuple[VoteTarget, ...]]]
