import itertools
import typing

from .maths import Matrix
from ..ballot import Ballot
from ...pd_types import VoteTarget, VotingResult

DEBUG = False


class VotingSystem:
    def iter_ballots(
        self, ballots: typing.Iterable[Ballot]
    ) -> list[tuple[int, tuple[VoteTarget, ...]]]:
        raise NotImplementedError


class Simple(VotingSystem):
    def __init__(self, keys: list[VoteTarget]):
        self.keys: list[VoteTarget] = keys

    def _make_matrix(self, ballot: Ballot) -> Matrix:
        # Matrix of dimension N x N where N is count of available voting targets.
        # Each cell represents a result from a match between runner and opponent.
        # Rows are runners, columns are opponents.
        # For more info, see https://en.wikipedia.org/wiki/Condorcet_method#Basic_procedure
        m = Matrix(len(self.keys))
        if DEBUG:
            print("Runner vs. opponent: rank => winner")

        for runner_index, runner in enumerate(self.keys):
            runner_vote = ballot.get_vote(runner)
            for opponent_index, opponent in enumerate(self.keys):
                if opponent == runner:
                    continue
                opponent_vote = ballot.get_vote(opponent)

                if DEBUG:
                    print(
                        f"{runner} ({runner_index}.) vs. {opponent} ({opponent_index}):"
                        f" {runner_vote} – {opponent_vote}"
                        " =>",
                        runner
                        if runner_vote > opponent_vote
                        else opponent
                        if runner_vote < opponent_vote
                        else "TIE",
                    )

                if runner_vote < opponent_vote:
                    m.set(runner_index, opponent_index, 1)
                elif runner_vote > opponent_vote:
                    m.set(opponent_index, runner_index, 1)
                # else: do nothing on tie.
        if DEBUG:
            print("Pairwise winner matrix:")
            print(m)
        return m

    def iter_ballots(self, ballots: typing.Iterable[Ballot]) -> VotingResult:
        if not self.keys:
            return []

        sum_matrix = Matrix(len(self.keys))
        for b in ballots:
            bm = self._make_matrix(b)
            sum_matrix.add_to_self(bm)

        return self._calculate(sum_matrix)

    def _calculate(
        self, sum_matrix: Matrix
    ) -> list[tuple[int, tuple[VoteTarget, ...]]]:
        # Calculate scores (row sum) for each runner (row).
        # e.g. [3, 8, 3]
        sums = sum_matrix.row_sums()

        # Make a pairwise list of row score and row key
        # e.g. [(3, 620), (8, 550), (3, 560)]
        sums_and_keys = list(zip(sums, self.keys))

        # Sort in descending order the row score-key pairs by their score
        # e.g. [(8, 550), (3, 560), (3, 620)]
        sums_and_keys.sort(key=_z_key_desc)

        # Group the pairs by their score. Result is "list" of lists of score-key pairs.
        # e.g. (
        #   (8, [(8, 550)]),
        #   (3, [(3, 560), (3, 620)]),
        # )
        groups = itertools.groupby(sums_and_keys, key=_z_key)

        # Reshape the result to be a "list" of tuples containing score and tuple of keys.
        # e.g. [
        #   (8, (550,)),
        #   (3, (560, 620)),
        # ]
        shaped = list((k, list(zip(*g))[1]) for k, g in groups)
        return shaped


def _z_key_desc(e: tuple[int, int]) -> int:
    return -e[0]


def _z_key(e: tuple[int, int]) -> int:
    return e[0]
