from __future__ import annotations

import typing


class Matrix:
    def __init__(self, side: int, mat: list[int] | None = None):
        # list of cells, column of a row at a time.
        self._matrix = ([0] * (side * side)) if mat is None else mat
        assert len(self._matrix) == side * side
        self._side = side

    def get(self, row: int, col: int) -> int:
        """
        Get the value of a cell.
        """
        assert col < self._side
        return self._matrix[row * self._side + col]

    def set(self, row: int, col: int, value: int) -> None:
        """
        Set a value of a cell.
        """
        assert col < self._side
        self._matrix[row * self._side + col] = value

    def add(self, other: Matrix) -> Matrix:
        """
        Sum cell-values of other matrix to a new matrix.

            1 2  +  3 5  =  4 7
            3 4     4 1     7 5

        >>> list(Matrix(2, [1, 2, 3, 4]).add(Matrix(2, [3, 5, 4, 1])))
        [4, 7, 7, 5]
        """
        r = self.__class__(self._side)
        for cell in range(self._side * self._side):
            r._matrix[cell] = self._matrix[cell] + other._matrix[cell]
        return r

    def add_to_self(self, other: Matrix) -> None:
        """
        Sum cell-values of other matrix, modifying self.

            1 2  +  3 5  =  4 7
            3 4     4 1     7 5
        """
        assert self._side == other._side, "Matrices are of different dimensions"
        for cell in range(self._side * self._side):
            self._matrix[cell] = self._matrix[cell] + other._matrix[cell]

    def row_sums(self) -> list[int]:
        """
        Calculate sum of each row.

        E.g. if 2 by 2 matrix is

            1 2
            3 4

        Returned list would be

            3, 7

        >>> Matrix(2, [1, 2, 3, 4]).row_sums()
        [3, 7]
        """
        return [
            sum(self._matrix[row_start : row_start + self._side])
            for row_start in range(0, self._side * self._side, self._side)
        ]

    def diagonal_wins(self) -> list[int]:
        """
        Calculate wins of cross-diagonal pairs.

            0 1 2 3
            1 0 2 0
            1 1 0 0
            1 1 1 0

        Would return

            2, 1, 0, 2

        >>> Matrix(4, [0, 1, 2, 3, 1, 0, 2, 0, 1, 1, 0, 0, 1, 1, 1, 0]).diagonal_wins()
        [2, 1, 0, 2]
        """
        return [
            sum(
                1 if self.get(row, col) > self.get(col, row) else 0
                for col in range(self._side)
            )
            for row in range(self._side)
        ]

    def __iter__(self) -> typing.Iterator[int]:
        return iter(self._matrix)

    def __str__(self):
        return "\n".join(
            ", ".join(str(self._matrix[row_start + col]) for col in range(self._side))
            + " = "
            + str(sum(self._matrix[row_start : row_start + self._side]))
            for row_start in range(0, self._side * self._side, self._side)
        )
