import unittest
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from snake_hamiltonian_cycle.snake import (
    EMPTY_NODE_ID,
    SNAKE_HEAD_ID,
    SNAKE_NODE_ID,
    APPLE_ID,
    SPIKE_ID,
    Snake_Node,
    move_snake,
    get_board_with_snake,
)


class TestSnake(unittest.TestCase):

    def test_move_snake(self):
        snake = [Snake_Node(y=0, x=0), Snake_Node(y=1, x=0), Snake_Node(y=2, x=0)]

        snake_move_grid = [
            [1, 2, 19, 20, 21, 22],
            [0, 3, 18, 17, 16, 23],
            [35, 4, 13, 14, 15, 24],
            [34, 5, 12, 11, 10, 25],
            [33, 6, 7, 8, 9, 26],
            [32, 31, 30, 29, 28, 27],
        ]
        grid = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]

        move_snake(snake=snake, move_grid=snake_move_grid, game_board=grid)

        # move to the right
        assert snake[0].x == 1
        assert snake[0].y == 0
        # takes place of the previous head (0,0)
        assert snake[1].x == 0
        assert snake[1].y == 0
        # takes place of the previous body (1,0)
        assert snake[2].x == 0
        assert snake[2].y == 1

    def test_move_snake_skip(self):
        snake = [Snake_Node(y=2, x=1), Snake_Node(y=1, x=1), Snake_Node(y=0, x=1)]
        move_grid = [[0, 1, 6, 7], [16, 2, 5, 8], [14, 3, 4, 9], [13, 12, 11, 10]]
        grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        move_snake(snake=snake, move_grid=move_grid, game_board=grid)

        # move to the right
        assert snake[0].x == 1
        assert snake[0].y == 3

    def test_get_board_with_snake(self):
        snake = [Snake_Node(y=0, x=0), Snake_Node(y=1, x=0), Snake_Node(y=2, x=0)]
        board = [[EMPTY_NODE_ID for _ in range(3)] for _ in range(3)]
        board = get_board_with_snake(snake=snake, board=board)

        # Snake
        assert board[0][0] == SNAKE_HEAD_ID
        assert board[1][0] == SNAKE_NODE_ID
        assert board[2][0] == SNAKE_NODE_ID
        # Empty
        assert board[0][1] == EMPTY_NODE_ID
        assert board[1][1] == EMPTY_NODE_ID
        assert board[2][1] == EMPTY_NODE_ID
        assert board[0][2] == EMPTY_NODE_ID
        assert board[1][2] == EMPTY_NODE_ID
        assert board[2][2] == EMPTY_NODE_ID


if __name__ == "__main__":
    unittest.main()
