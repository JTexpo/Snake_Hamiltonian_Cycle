import unittest
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from snake_hamiltonian_cycle.hamiltonian import (
    get_hamiltonian_cycle,
    draw_hamiltonian_cycle,
)


class TestHamiltonian(unittest.TestCase):

    def test_get_hamiltonian_cycle(self):
        grid = [
            [False, False, False, False],
            [False, False, False, False],
            [False, False, False, False],
            [False, False, False, False],
        ]

        paths = get_hamiltonian_cycle(
            grid=grid, blocked_tiles=0, start_x=0, start_y=0, end_x=0, end_y=1, path=[(0, 0)]
        )

        expected = [
            (0, 0),
            (0, 1),
            (1, 1),
            (2, 1),
            (2, 2),
            (1, 2),
            (0, 2),
            (0, 3),
            (1, 3),
            (2, 3),
            (3, 3),
            (3, 2),
            (3, 1),
            (3, 0),
            (2, 0),
            (1, 0),
        ]

        self.assertEqual(len(paths), len(expected))
        for path_index, path in enumerate(paths):
            self.assertEqual(path, expected[path_index])

    def test_draw_hamiltonian_cycle(self):
        hamiltonian_moves = [
            (0, 0),
            (0, 1),
            (1, 1),
            (2, 1),
            (2, 2),
            (1, 2),
            (0, 2),
            (0, 3),
            (1, 3),
            (2, 3),
            (3, 3),
            (3, 2),
            (3, 1),
            (3, 0),
            (2, 0),
            (1, 0),
        ]

        hamiltonian_cycle = draw_hamiltonian_cycle(
            hamiltonian_cycle=hamiltonian_moves, board_length=4, board_width=4
        )

        excepted = [[0, 1, 6, 7], [15, 2, 5, 8], [14, 3, 4, 9], [13, 12, 11, 10]]

        for row_index, row in enumerate(hamiltonian_cycle):
            for col_index, col in enumerate(row):
                self.assertEqual(col, excepted[row_index][col_index])


if __name__ == "__main__":
    unittest.main()
