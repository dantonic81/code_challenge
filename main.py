from typing import List, Tuple, Set


upper_alpha = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


def create_map_arr(map_str) -> List[List[str]]:
    """
    Converts a string representation of a map to a two-dimensional list of characters.

    The input string should contain only the following characters:
    - uppercase letters ('A' to 'Z')
    - special characters ('x', '@', '-', '|', '+', '\n', ' ') representing the start, end, corners, empty spaces etc.
    The function will raise a ValueError if the input string contains any other characters.

    The input string should contain exactly one '@' character representing the starting position, and one or more 'x'
    characters representing the ending position. The function will raise a ValueError if either of these characters is
    missing or if there are multiple '@' characters in the input string.

    The function will pad the rows of the two-dimensional list with spaces to make all rows have the same length, and
    return a rectangular map where each character corresponds to one cell in the grid.

    Parameters:
    map_str (str): a string representation of a map

    Returns:
    A two-dimensional list of characters representing the map
    """
    allowed = {'x', '@', '-', '|', '+', '\n', ' '}

    # check if map contains invalid characters
    invalid_chars = set(map_str) - upper_alpha - allowed
    if invalid_chars:
        raise ValueError(f'Map contains invalid characters: {", ".join(invalid_chars)}')

    # check for missing start character
    if '@' not in map_str:
        raise ValueError('Map has no start!')

    # check for multiple start characters
    if map_str.count('@') > 1:
        raise ValueError('Map has multiple starts!')

    # check for missing end character
    if 'x' not in map_str:
        raise ValueError('Map has no end!')

    # Split the string into a list of strings, where each string represents a row in the map
    map_list = map_str.split('\n')

    # Remove any empty strings from the list
    map_list = list(filter(None, map_list))

    # pad rows with spaces if jagged
    map_list = [row.ljust(max(map(len, map_list)), ' ') for row in map_list]

    # convert strings to lists
    map_list = [list(i) for i in map_list]

    return map_list


# TRAVERSE MAP LOGIC
def _find_start(arr):
    for x, row in enumerate(arr):
        for y, char in enumerate(row):
            if char == '@':
                return x, y


def _move(arr, pos, direction):
    x, y = pos
    if direction == 'left':
        next_pos = (x, y - 1)
    elif direction == 'right':
        next_pos = (x, y + 1)
    elif direction == 'up':
        next_pos = (x - 1, y)
    elif direction == 'down':
        next_pos = (x + 1, y)

    next_char = arr[next_pos[0]][next_pos[1]]
    if next_char in {'-', '|', '+', 'x'} | upper_alpha:
        return next_pos
    else:
        raise ValueError(f'Invalid move to position {next_pos}')


def _explore_directions(arr, pos):
    x, y = pos
    valid_movement = {'left': {'can_move': False, 'position': (), 'character': arr[x][y - 1] if y != 0 else None},
                      'right': {'can_move': False, 'position': (),
                                'character': arr[x][y + 1] if y < len(arr[0]) - 1 else None},
                      'up': {'can_move': False, 'position': (), 'character': arr[x - 1][y] if x != 0 else None},
                      'down': {'can_move': False, 'position': (),
                               'character': arr[x + 1][y] if x < len(arr) - 1 else None}}

    if arr[x][y - 1] in {'-', 'x', '+'} | upper_alpha and y != 0:
        valid_movement['left']['can_move'] = True
        valid_movement['left']['position'] = (x, y - 1)

    if y < len(arr[0]) - 1 and arr[x][y + 1] in {'-', 'x', '+'} | upper_alpha:
        valid_movement['right']['can_move'] = True
        valid_movement['right']['position'] = (x, y + 1)

    if x != 0 and arr[x - 1][y] in {'|', 'x', '+', '-'} | upper_alpha:
        valid_movement['up']['can_move'] = True
        valid_movement['up']['position'] = (x - 1, y)

    if x < len(arr) - 1 and arr[x + 1][y] in {'|', 'x', '+', '-'} | upper_alpha:
        valid_movement['down']['can_move'] = True
        valid_movement['down']['position'] = (x + 1, y)

    valid_movement = {k: v for (k, v) in valid_movement.items() if v['can_move']}

    return valid_movement

def traverse_map(map_arr):
    """
    Traverse the map and return the collected letters, path, and visited locations.

    Args:
        map_arr (list): A list of lists representing the map.

    Returns:
        Tuple[str, List[str], Set[Tuple[int, int]]]: A tuple containing the collected letters, path, and visited locations.
    """
    start_pos = _find_start(map_arr)
    visited = set()
    stack = [start_pos]
    last_direction = None
    locations_picked = []
    letters = []
    path = []
    opposite_direction = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}

    while stack:
        pos = stack.pop()
        if pos in visited:
            continue
        visited.add(pos)
        x, y = pos
        current_pos = map_arr[x][y]
        back = opposite_direction.get(last_direction)
        path.append(current_pos)
        if current_pos == 'x':
            return ''.join(letters), ''.join(path)

        if current_pos in upper_alpha and pos not in locations_picked:
            letters.append(current_pos)
            locations_picked.append(pos)
        directions = _explore_directions(map_arr, pos)

        unvisited_directions = {k: v for (k, v) in directions.items() if v['position'] not in visited}

        num_directions = sum(
            [direction['can_move'] for direction in unvisited_directions.values() if direction['can_move']])

        if num_directions == 0:
            if len(directions) == 1 and opposite_direction[back] == direction:
                raise ValueError('Broken path!')

            # handling cases when only options have all been visited
            has_move = any(v['can_move'] for v in unvisited_directions.values())
            if not has_move:
                can_move = {k: v for (k, v) in directions.items() if v['can_move']}
                all_visited = {k: v for (k, v) in can_move.items() if v['position'] in visited}
                if all_visited and len(all_visited) == len(can_move):
                    for direction in all_visited:
                        dir_location_x, dir_location_y = all_visited[direction]['position']
                        if map_arr[dir_location_x][dir_location_y] not in ['x', '@', '+']:
                            visited.remove(all_visited[direction]['position'])
                            stack.append(all_visited[direction]['position'])
                            break
                    continue

        elif num_directions == 1:
            for direction, status in unvisited_directions.items():
                if status['can_move']:
                    next_pos = _move(map_arr, pos, direction)
                    stack.append(next_pos)
                    if current_pos == '+' and direction == last_direction:
                        raise ValueError('Fake turn!')
                    last_direction = direction
        elif num_directions > 1:
            if current_pos == '+':
                raise ValueError('Fork in path!')
            if current_pos == '@':
                raise ValueError('Multiple starting paths!')
            for direction, status in unvisited_directions.items():
                if status['can_move'] and direction == last_direction:
                    next_pos = _move(map_arr, pos, direction)
                    stack.append(next_pos)
                    last_direction = direction




# print(traverse_map(create_map_arr(intersections)))

