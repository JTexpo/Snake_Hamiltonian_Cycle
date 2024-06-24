from typing import List
import asyncio

from js import document
from pyodide.ffi import create_proxy
import pyscript
from pyscript import Element

from snake_hamiltonian_cycle.snake import (
    EMPTY_NODE_ID,
    SNAKE_HEAD_ID,
    SNAKE_NODE_ID,
    APPLE_ID,
    SPIKE_ID,
    Snake_Node,
    get_board_with_snake,
    move_snake,
)
from snake_hamiltonian_cycle.hamiltonian import (
    get_hamiltonian_cycle,
    draw_hamiltonian_cycle,
)

LINE_WIDTH = 2
SPACING = 6

BOARD_LENGTH = 6
BOARD_WIDTH = 6

COLOUR_MAPPING = {
    EMPTY_NODE_ID: "white",
    SNAKE_HEAD_ID: "cyan",
    SNAKE_NODE_ID: "blue",
    APPLE_ID: "red",
    SPIKE_ID: "black",
}

APPLE_MODE_KEY = 1
ERASE_MODE_KEY = 2
SPIKES_MODE_KEY = 3

MODE = APPLE_MODE_KEY

GAME_SPEED = 0.3

SNAKE_GAME_ID = "snake-game"

draw_snake_move = False

game_board: List[List[int]] = [
    [EMPTY_NODE_ID for _ in range(BOARD_LENGTH)] for _ in range(BOARD_WIDTH)
]
game_board_spikes: List[List[int]] = [
    [EMPTY_NODE_ID for _ in range(BOARD_LENGTH)] for _ in range(BOARD_WIDTH)
]
snake: List[Snake_Node] = [
    Snake_Node(y=0, x=0),
    Snake_Node(y=1, x=0),
    Snake_Node(y=2, x=0),
]
snake_move_grid: List[List[int]] = [
    [0, 1, 18, 19, 20, 21],
    [35, 2, 17, 16, 15, 22],
    [34, 3, 12, 13, 14, 23],
    [33, 4, 11, 10, 9, 24],
    [32, 5, 6, 7, 8, 25],
    [31, 30, 29, 28, 27, 26],
]

'''
--------------
GAME FUNCTIONS
--------------
'''
def get_new_path():
    """A function to get a new path for the snake to follow"""
    global snake, snake_move_grid, game_board_spikes

    # We are getting the board with the snake so that we can know the existing path of the snake,
    # to make the process of finding a hamiltonian cycle easier as well as fluid,
    # as the cycle will always connect from head to tail
    move_grid_view_board = get_board_with_snake(snake=snake, board=game_board_spikes)

    # For the hamiltonian cycle, we are setting the head and tail to empty
    move_grid_view_board[snake[-1].y][snake[-1].x] = EMPTY_NODE_ID

    # Getting the number of spikes, to help on some edge cases where we could be faster.
    # Notably, when there is 1 spike on a 6x6, we know the cycle should be 34 tiles,
    # as on a grid we can not have an odd number of tiles in a hamiltonian cycle
    spike_count = sum([1 for row in game_board_spikes for x in row if x == SPIKE_ID])

    hamiltonian_cycle = get_hamiltonian_cycle(
        grid=move_grid_view_board,
        blocked_tiles=spike_count,
        start_x=snake[0].x,
        start_y=snake[0].y,
        end_x=snake[-1].x,
        end_y=snake[-1].y,
        path=[(snake.y, snake.x) for snake in list(snake)[::-1][1:]],
    )

    snake_move_grid = draw_hamiltonian_cycle(
        hamiltonian_cycle=hamiltonian_cycle,
        board_length=BOARD_LENGTH,
        board_width=BOARD_WIDTH,
    )

'''
--------------
VIEW FUNCTIONS
--------------
'''
def clear_board():
    """
    Clear the game board by filling it with black, then drawing a white rectangle
    inside filled with black lines to represent the game board grid.

    Args:
        reset_board (bool, optional): If True, reset the game board to a new blank
            board. Default is True.
    """
    global LINE_WIDTH, SPACING, BOARD_WIDTH, BOARD_LENGTH, SNAKE_GAME_ID, game_board, game_board_spikes, snake, snake_move_grid

    # Reset the game board
    game_board = [
        [EMPTY_NODE_ID for _ in range(BOARD_LENGTH)] for _ in range(BOARD_WIDTH)
    ]
    game_board_spikes = [
        [EMPTY_NODE_ID for _ in range(BOARD_LENGTH)] for _ in range(BOARD_WIDTH)
    ]

    # Reset the snake
    snake = [
        Snake_Node(y=0, x=0),
        Snake_Node(y=1, x=0),
        Snake_Node(y=2, x=0),
    ]

    # Reset the snake move grid
    snake_move_grid = [
        [0, 1, 18, 19, 20, 21],
        [35, 2, 17, 16, 15, 22],
        [34, 3, 12, 13, 14, 23],
        [33, 4, 11, 10, 9, 24],
        [32, 5, 6, 7, 8, 25],
        [31, 30, 29, 28, 27, 26],
    ]

    # Clear the game board game view and drawling the grid
    canvas = document.getElementById(SNAKE_GAME_ID)
    ctx = canvas.getContext("2d")

    # Black background
    ctx.fillStyle = "black"
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    # White mini-background
    ctx.fillStyle = "white"
    ctx.fillRect(
        LINE_WIDTH,
        LINE_WIDTH,
        canvas.width - LINE_WIDTH * 2,
        canvas.height - LINE_WIDTH * 2,
    )

    # Black lines vertical
    ctx.fillStyle = "black"
    for index in range(1, SPACING):
        ctx.fillRect(
            index * (canvas.width / SPACING) - LINE_WIDTH,
            0,
            LINE_WIDTH * 2,
            canvas.height,
        )

    # Black lines horizontal
    for index in range(1, SPACING * 2):
        ctx.fillRect(
            0,
            index * (canvas.height / SPACING) - LINE_WIDTH,
            canvas.width,
            LINE_WIDTH * 2,
        )

def draw_board(board: List[List[int]]):
    """
    Draw the given board on the canvas starting from the specified index.

    Args:
        board (List[List[int]]): The board to be drawn.
    """
    global LINE_WIDTH, SPACING, COLOUR_MAPPING, SNAKE_GAME_ID, draw_snake_move

    canvas = document.getElementById(SNAKE_GAME_ID)
    ctx = canvas.getContext("2d")

    for y, row in enumerate(board):
        for x, value in enumerate(row):

            if value != EMPTY_NODE_ID:
                continue

            ctx.fillStyle = COLOUR_MAPPING[value]

            ctx.fillRect(
                x * (canvas.width / SPACING) + LINE_WIDTH,
                y * (canvas.height / SPACING) + LINE_WIDTH,
                canvas.width / SPACING - LINE_WIDTH * 2,
                canvas.height / SPACING - LINE_WIDTH * 2,
            )

    if draw_snake_move:
        draw_snake_moves()

    for y, row in enumerate(board):
        for x, value in enumerate(row):

            if value == EMPTY_NODE_ID:
                continue

            ctx.fillStyle = COLOUR_MAPPING[value]

            ctx.fillRect(
                x * (canvas.width / SPACING) + LINE_WIDTH,
                y * (canvas.height / SPACING) + LINE_WIDTH,
                canvas.width / SPACING - LINE_WIDTH * 2,
                canvas.height / SPACING - LINE_WIDTH * 2,
            )

def draw_snake_moves():
    global snake_move_grid, SNAKE_GAME_ID

    # Clear the game board game view and drawling the grid
    canvas = document.getElementById(SNAKE_GAME_ID)
    ctx = canvas.getContext("2d")

    ctx.fillStyle = "orange"
    ctx.font = "50px Arial"
    for y_index, row in enumerate(snake_move_grid):
        for x_index, move in enumerate(row):
            if move >= 0:
                ctx.fillText(
                    move,
                    (canvas.width / SPACING) * x_index + (canvas.width / SPACING) / 4,
                    (canvas.height / SPACING) * (y_index + 1)
                    - (canvas.height / SPACING) / 4,
                )

'''
----------------
BUTTON FUNCTIONS
----------------
'''
def reset():
    clear_board()

def toggle_mode(mode: int):
    global MODE
    MODE = mode

def toggle_snake_move_view():
    global draw_snake_move
    draw_snake_move = not draw_snake_move

'''
----
MAIN
----
'''
async def main():
    """
    Asynchronous main function that runs indefinitely.
    """
    global game_board, COLOUR_MAPPING, GAME_SPEED, snake
    while True:
        # Move the snake
        move_snake(snake=snake, move_grid=snake_move_grid, game_board=game_board)
        # Check if the snake has eaten the apple
        if game_board[snake[0].y][snake[0].x] == APPLE_ID:
            snake.append(Snake_Node(y=snake[-1].y, x=snake[-1].x))
            game_board[snake[0].y][snake[0].x] = EMPTY_NODE_ID
        # Draw the game board
        draw_board(board=get_board_with_snake(snake=snake, board=game_board))

        # Give the user time to see the new game state
        await asyncio.sleep(GAME_SPEED)


def _on_click(element):
    global game_board, snake_move_grid, game_board_spikes, SPACING, MODE, APPLE_MODE_KEY, ERASE_MODE_KEY, SPIKES_MODE_KEY, APPLE_ID, SPIKE_ID, EMPTY_NODE_ID, SNAKE_GAME_ID

    canvas = document.getElementById(SNAKE_GAME_ID)

    # APPLE
    # -----
    if MODE == APPLE_MODE_KEY:
        game_board[int(element.offsetY // (canvas.width / SPACING))][
            int(element.offsetX // (canvas.width / SPACING))
        ] = APPLE_ID

    # DRAW
    # ----
    if MODE == SPIKES_MODE_KEY:
        game_board[int(element.offsetY // (canvas.width / SPACING))][
            int(element.offsetX // (canvas.width / SPACING))
        ] = SPIKE_ID
        game_board_spikes[int(element.offsetY // (canvas.width / SPACING))][
            int(element.offsetX // (canvas.width / SPACING))
        ] = SPIKE_ID
        get_new_path()

    # ERASE
    # -----
    elif MODE == ERASE_MODE_KEY:
        game_board[int(element.offsetY // (canvas.width / SPACING))][
            int(element.offsetX // (canvas.width / SPACING))
        ] = EMPTY_NODE_ID
        game_board_spikes[int(element.offsetY // (canvas.width / SPACING))][
            int(element.offsetX // (canvas.width / SPACING))
        ] = EMPTY_NODE_ID
        get_new_path()


# initalize the game
clear_board()
draw_board(board=get_board_with_snake(snake=snake, board=game_board))

# add event listeners
on_click = create_proxy(_on_click)
document.getElementById(SNAKE_GAME_ID).addEventListener("mousedown", on_click)
pyscript.run_until_complete(main())
