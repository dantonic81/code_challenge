import string
from typing import Dict, List, Tuple
from utils.exceptions import BrokenPathError, FakeTurnError, ForkInPathError, MultipleStartingPathsError, \
    InvalidDirectionError, InvalidMapError

UPPER_ALPHA = set(string.ascii_uppercase)


def create_map_array(map_str) -> List[List[str]]:
    """
    Converts a string representation of a map to a two-dimensional list of characters.

    The input string should contain only the following characters:
    - uppercase letters ('A' to 'Z')
    - special characters ('x', '@', '-', '|', '+', '\n', ' ') representing the start, end, corners, empty spaces etc.
    The function will raise an InvalidMapError if the input string contains any other characters.

    The input string should contain exactly one '@' character representing the starting position, and one or more 'x'
    characters representing the ending position. The function will raise an InvalidMapError if either of these characters is
    missing or if there are multiple '@' characters in the input string.

    The function will pad the rows of the two-dimensional list with spaces to make all rows have the same length, and
    return a rectangular map where each character corresponds to one cell in the grid.

    Parameters:
    map_str (str): a string representation of a map

    Returns:
    A two-dimensional list of characters representing the map
    """
    allowed_chars = UPPER_ALPHA.union({'x', '@', '-', '|', '+', '\n', ' '})
    invalid_chars = set(map_str) - allowed_chars
    if invalid_chars:
        raise InvalidMapError(f'Map contains invalid characters: {", ".join(invalid_chars)}')

    if '@' not in map_str:
        raise InvalidMapError('Missing start position "@" in map!')
    elif map_str.count('@') > 1:
        raise InvalidMapError('Multiple start positions "@" in map!')

    if 'x' not in map_str:
        raise InvalidMapError('Missing end position "x" in map!')

    rows = map_str.splitlines()
    jagged_rows = [row for row in rows if row]
    justified_rows = [row.ljust(max(map(len, jagged_rows)), ' ') for row in jagged_rows]
    map_array = [list(i) for i in justified_rows]

    return map_array


# TRAVERSE MAP LOGIC
def _find_start(map_array: List[List[str]]) -> Tuple[int, int]:
    for x, row in enumerate(map_array):
        for y, char in enumerate(row):
            if char == '@':
                return x, y
    raise InvalidMapError('Start position not found!')


def _move(map_array: List[List[str]], position: Tuple[int, int], direction: str) -> Tuple[int, int]:
    x, y = position
    try:
        dx, dy = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }[direction]
    except KeyError as e:
        raise InvalidDirectionError(f"Direction {e} not allowed!")
    return x + dx, y + dy


def _get_valid_moves(map_array: List[List[str]], position: Tuple[int, int]) -> Dict[str, Dict[str, object]]:
    x, y = position
    left_col, right_col = y-1, y+1
    up_row, down_row = x-1, x+1

    left_char = map_array[x][left_col] if y != 0 else None
    right_char = map_array[x][right_col] if y < len(map_array[0]) - 1 else None
    up_char = map_array[up_row][y] if x != 0 else None
    down_char = map_array[down_row][y] if x < len(map_array) - 1 else None

    moves = {
        'left': {'can_move': left_char in {'-', 'x', '+'} | UPPER_ALPHA, 'position': (x, left_col), 'character': left_char},
        'right': {'can_move': right_char in {'-', 'x', '+'} | UPPER_ALPHA, 'position': (x, right_col), 'character': right_char},
        'up': {'can_move': up_char in {'|', 'x', '+', '-'} | UPPER_ALPHA, 'position': (up_row, y), 'character': up_char},
        'down': {'can_move': down_char in {'|', 'x', '+', '-'} | UPPER_ALPHA, 'position': (down_row, y), 'character': down_char}
    }

    moves = {k: v for (k, v) in moves.items() if v['can_move']}

    return moves


def traverse_map(map_array: List[List[str]]) -> Tuple[str, str]:
    """
    Traverse the map and return the collected letters and path.

    Args:
        map_array (list): A list of lists representing the map.

    Returns:
        Tuple[str, List[str]]: A tuple containing the collected letters and path.
    """
    if not map_array or not all(len(row) == len(map_array[0]) for row in map_array):
        raise InvalidMapError('Invalid map: not a rectangular grid of characters!')

    unvisited_direction = None
    opposite_direction = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
    start_pos = _find_start(map_array)
    visited = set()
    stack = [start_pos]
    last_direction = None
    locations_picked = set()
    letters = []
    path = []

    while stack:
        position = stack.pop()
        visited.add(position)
        x, y = position
        current_cell = map_array[x][y]
        back = opposite_direction.get(last_direction)
        path.append(current_cell)

        if current_cell in UPPER_ALPHA and position not in locations_picked:
            letters.append(current_cell)
            locations_picked.add(position)

        if current_cell == 'x':
            return f'{"".join(letters)}', f'{"".join(path)}'

        directions = _get_valid_moves(map_array, position)

        unvisited_directions = {k: v for (k, v) in directions.items() if v['position'] not in visited}

        if len(unvisited_directions) == 0:
            if len(directions) == 1 and opposite_direction[back] == unvisited_direction:
                raise BrokenPathError('Broken path!')

            # handling case when all valid moves have been visited
            all_visited = {k: v for (k, v) in directions.items() if v['position'] in visited}
            if all_visited and len(all_visited) == len(directions):
                for visited_direction in all_visited:
                    dir_location_x, dir_location_y = all_visited[visited_direction]['position']
                    if map_array[dir_location_x][dir_location_y] not in ['x', '@', '+']:
                        visited.remove(all_visited[visited_direction]['position'])
                        stack.append(all_visited[visited_direction]['position'])
                        break
                continue

        elif len(unvisited_directions) == 1:
            for unvisited_direction, _ in unvisited_directions.items():
                next_pos = _move(map_array, position, unvisited_direction)
                stack.append(next_pos)
                if current_cell == '+' and unvisited_direction == last_direction:
                    raise FakeTurnError('Fake turn!')
                last_direction = unvisited_direction

        else:
            if current_cell == '+':
                raise ForkInPathError('Fork in path!')
            elif current_cell == '@':
                raise MultipleStartingPathsError('Multiple starting paths!')
            for unvisited_direction, _ in unvisited_directions.items():
                if unvisited_direction == last_direction:
                    next_pos = _move(map_array, position, unvisited_direction)
                    stack.append(next_pos)
                    last_direction = unvisited_direction


if __name__ == '__main__':
    # Example map string
    map_str = """
      @---A---+
              |
      x-B-+   C
          |   |
          +---+
    """

    # Convert the string representation of the map to a two-dimensional list
    map_array = create_map_array(map_str)

    # Traverse the map and get the collected letters and path
    letters, path = traverse_map(map_array)

    print(f"Letters: {letters}")
    print(f"Path: {path}")
