from typing import List


def find_hamiltonian_cycle(
    grid: List[List[bool]],
    blocked_tiles: int,
    x: int,
    y: int,
    path: List[int],
    paths: List[List[int]],
    end_x: int,
    end_y: int,
) -> None:
    """A recursive function to find all the paths in a given grid

    Args:
        grid (List[List[bool]]): the retangular grid to search in
        blocked_tiles (int): the number of blocked tiles in the grid
        x (int): starting x coordinate
        y (int): starting y coordinate
        path (List[int]): a list of coordinates that the snake has traversed
        paths (List[List[int]]): a list of paths
        end_x (int): ending x coordinate
        end_y (int): ending y coordinate
    
    Returns:
        None
    
    Raises:
        AssertionError: if we have found the first hamiltonian cycle, this is to stop the recursion as quickly as possible
    """

    # if we have reached the end
    if x == end_x and y == end_y:
        paths.append(list(path))

        # Find the longest path length
        longest_path = max(len(found_path) for found_path in paths)
        # Remove all paths that are not the longest
        for found_path in paths:
            if len(found_path) < longest_path:
                paths.remove(found_path)

        # Check if we have found the first hamiltonian cycle, if so, raise an error to stop the recursion
        # NOTE: there are other ways to end the recursion; however, this is the 'fastest' one I chose
        if longest_path == (len(grid) * len(grid[0]) - blocked_tiles) - (
            (len(grid) * len(grid[0]) - blocked_tiles) % 2
        ):
            raise AssertionError("Fond first hamiltonian cycle")

        return

    # Try moving down, right, up, left
    for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        # Check if the move is valid
        new_x: int = x + dx
        new_y: int = y + dy
        # Check if the move is valid
        if (
            0 <= new_y < len(grid)
            and 0 <= new_x < len(grid[0])
            and not grid[new_y][new_x]
        ):
            # Mark the current cell as visited
            grid[new_y][new_x] = True
            find_hamiltonian_cycle(
                grid=grid,
                blocked_tiles=blocked_tiles,
                x=new_x,
                y=new_y,
                path=path + [(new_y, new_x)],
                paths=paths,
                end_x=end_x,
                end_y=end_y,
            )
            grid[new_y][new_x] = False


def get_hamiltonian_cycle(
    grid: List[List[bool]],
    blocked_tiles: int,
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    path: List[int],
) -> List[List[int]]:
    """Function to get all the paths in a given grid

    Args:
        grid (List[List[bool]]): the retangular grid to search in
        blocked_tiles (int): the number of blocked tiles in the grid
        start_x (int): the starting x coordinate
        start_y (int): the starting y coordinate
        end_x (int): the ending x coordinate
        end_y (int): the ending y coordinate
        path (List[int], optional): a list of coordinates that the snake has traversed.

    Returns:
        List[List[int]]: the list of cordinates that the snake has traversed
    
    Raises:
        ValueError: if no paths are found
    """

    # Creating an empty list of paths, this value will be updated throughout the recursion instead of something being returned
    paths = []

    try:
        find_hamiltonian_cycle(
            grid=grid,
            blocked_tiles=blocked_tiles,
            x=start_x,
            y=start_y,
            path=path,
            paths=paths,
            end_x=end_x,
            end_y=end_y,
        )
    except AssertionError:
        # NOTE: there are other ways to end the recursion; however, this is the 'fastest' one I chose
        pass

    # If no paths are found, raise an error
    if not paths:
        raise ValueError("No paths found")
    
    # Return the first path
    return paths[0]


def draw_hamiltonian_cycle(
    hamiltonian_cycle: List[List[int]], board_length: int, board_width: int
) -> List[List[int]]:
    """Function to draw the hamiltonian cycle

    Args:
        hamiltonian_cycle (List[List[int]]): 

    Returns:
        List[List[int]]: 
    """
    # Creating an empty board
    hamiltonian_board: List[List[int]] = [
        [-1 for _ in range(board_length)] for _ in range(board_width)
    ]

    # Drawing the hamiltonian cycle
    for move_index, node in enumerate(hamiltonian_cycle):
        hamiltonian_board[node[0]][node[1]] = move_index

    return hamiltonian_board
