from typing import List
from copy import deepcopy


# IDs
# ---
EMPTY_NODE_ID = 0
SNAKE_NODE_ID = 1
SNAKE_HEAD_ID = 2
APPLE_ID = 3
SPIKE_ID = 4


class Snake_Node:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

def move_snake(
    snake: List[Snake_Node], move_grid: List[List[int]], game_board: List[List[int]]
) -> None:
    """A function to move a snake in the direction of the hamiltonian cycle

    WARNING: This function mutates the snake

    Args:
        snake (Snake): the snake
        move_grid (List[List[int]]): a grid that shows the hamiltonian cycle for the snake to move along
        game_board (List[List[int]]): the game board, this is used to find the apple
    """
    # getting the current head index
    move_number = move_grid[snake[0].y][snake[0].x]

    # getting the number of the apple
    for apple_y, row in enumerate(game_board):
        if APPLE_ID in row:
            apple_number = move_grid[apple_y][row.index(APPLE_ID)]
            break
    else:
        apple_number = len(move_grid[0]) * len(move_grid)

    # moving all of the snake nodes to their new positions
    for i in range(len(snake) - 1, 0, -1):
        snake[i].x = snake[i - 1].x
        snake[i].y = snake[i - 1].y

    # finding the next number that the head should move to, to follow the hamiltonian cycle
    largest_move_number = max([max(move_row) for move_row in move_grid])
    if move_number == largest_move_number:
        move_number = 0
    else:
        greatest_skip = 0
        greatest_move_number = -1
        # check the left right up down, and if the delta of the current move to the next move is less than the size of the board minus the length of the snake, use that
        for delta in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            # get the next move
            new_x = snake[0].x + delta[0]
            new_y = snake[0].y + delta[1]
            # check if the next move is within the board
            if (
                new_x >= 0
                and new_x < len(move_grid[0])
                and new_y >= 0
                and new_y < len(move_grid)
            ):
                next_move_number = move_grid[new_y][new_x]
                # check if the delta is greater than the greatest skip, if it is, use that
                if (
                    (next_move_number - move_number > greatest_skip)
                    and (
                        next_move_number
                        < largest_move_number - len(snake)
                    )
                    and (apple_number not in range(move_number, next_move_number))
                ):
                    greatest_skip = next_move_number - move_number
                    greatest_move_number = next_move_number
            # this should only be triggered if the snake is the same length of the board
        if greatest_move_number == -1:
            move_number += 1
        else:
            move_number = greatest_move_number

    # moving the head
    for row_index, row in enumerate(move_grid):
        for move_index, row_move_number in enumerate(row):
            if move_number == row_move_number:
                snake[0].x = move_index
                snake[0].y = row_index


def get_board_with_snake(
    snake: List[Snake_Node], board: List[List[int]]
) -> List[List[int]]:
    """A function to add the snake to the board

    Args:
        snake (Snake): the snake
        board (List[List[int]]): a board that should have the snake, the apple, and the spikes

    Returns:
        List[List[int]]: updated board with a snake
    """
    # creating a deepcopy, so we don't alter the original board
    copy_of_board = deepcopy(board)

    # adding the snake nodes to the board
    for node in snake:
        copy_of_board[node.y][node.x] = SNAKE_NODE_ID

    # adding the head
    copy_of_board[snake[0].y][snake[0].x] = SNAKE_HEAD_ID

    return copy_of_board
