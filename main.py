import string
from typing import Dict, List, Tuple
from utils.exceptions import BrokenPathError, FakeTurnError, ForkInPathError, MultipleStartingPathsError, \
    InvalidMapError

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


def _move(map_array: List[List[str]], pos: Tuple[int, int], direction: str) -> Tuple[int, int]:
    x, y = pos
    dx, dy = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }[direction]
    return x + dx, y + dy


def _get_valid_moves(map_array: List[List[str]], pos: Tuple[int, int]) -> Dict[str, Dict[str, object]]:
    x, y = pos
    moves = {'left': {'can_move': False, 'position': (), 'character': map_array[x][y - 1] if y != 0 else None},
                      'right': {'can_move': False, 'position': (),
                                'character': map_array[x][y + 1] if y < len(map_array[0]) - 1 else None},
                      'up': {'can_move': False, 'position': (), 'character': map_array[x - 1][y] if x != 0 else None},
                      'down': {'can_move': False, 'position': (),
                               'character': map_array[x + 1][y] if x < len(map_array) - 1 else None}}

    if map_array[x][y - 1] in {'-', 'x', '+'} | UPPER_ALPHA and y != 0:
        moves['left']['can_move'] = True
        moves['left']['position'] = (x, y - 1)

    if y < len(map_array[0]) - 1 and map_array[x][y + 1] in {'-', 'x', '+'} | UPPER_ALPHA:
        moves['right']['can_move'] = True
        moves['right']['position'] = (x, y + 1)

    if x != 0 and map_array[x - 1][y] in {'|', 'x', '+', '-'} | UPPER_ALPHA:
        moves['up']['can_move'] = True
        moves['up']['position'] = (x - 1, y)

    if x < len(map_array) - 1 and map_array[x + 1][y] in {'|', 'x', '+', '-'} | UPPER_ALPHA:
        moves['down']['can_move'] = True
        moves['down']['position'] = (x + 1, y)

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

    start_pos = _find_start(map_array)
    visited = set()
    stack = [start_pos]
    last_direction = None
    locations_picked = set()
    letters = []
    path = []
    opposite_direction = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}

    while stack:
        pos = stack.pop()
        if pos in visited:
            continue
        visited.add(pos)
        x, y = pos
        current_position = map_array[x][y]
        back = opposite_direction.get(last_direction)
        path.append(current_position)
        if current_position == 'x':
            return ''.join(letters), ''.join(path)

        if current_position in UPPER_ALPHA and pos not in locations_picked:
            letters.append(current_position)
            locations_picked.add(pos)
        directions = _get_valid_moves(map_array, pos)

        unvisited_directions = {k: v for (k, v) in directions.items() if v['position'] not in visited}

        num_directions = sum([direction['can_move'] for direction in unvisited_directions.values() if direction['can_move']])

        if num_directions == 0:
            if len(directions) == 1 and opposite_direction[back] == direction:
                raise BrokenPathError('Broken path!')

            # handling cases when only options have all been visited
            has_move = any(v['can_move'] for v in unvisited_directions.values())
            if not has_move:
                can_move = {k: v for (k, v) in directions.items() if v['can_move']}
                all_visited = {k: v for (k, v) in can_move.items() if v['position'] in visited}
                if all_visited and len(all_visited) == len(can_move):
                    for direction in all_visited:
                        dir_location_x, dir_location_y = all_visited[direction]['position']
                        if map_array[dir_location_x][dir_location_y] not in ['x', '@', '+']:
                            visited.remove(all_visited[direction]['position'])
                            stack.append(all_visited[direction]['position'])
                            break
                    continue

        elif num_directions == 1:
            for direction, status in unvisited_directions.items():
                if status['can_move']:
                    next_pos = _move(map_array, pos, direction)
                    stack.append(next_pos)
                    if current_position == '+' and direction == last_direction:
                        raise FakeTurnError('Fake turn!')
                    last_direction = direction
        elif num_directions > 1:
            if current_position == '+':
                raise ForkInPathError('Fork in path!')
            elif current_position == '@':
                raise MultipleStartingPathsError('Multiple starting paths!')
            for direction, status in unvisited_directions.items():
                if status['can_move'] and direction == last_direction:
                    next_pos = _move(map_array, pos, direction)
                    stack.append(next_pos)
                    last_direction = direction


# print(traverse_map(create_map_array(intersections)))
