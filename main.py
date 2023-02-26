# basic example
test = """
  @---A---+
          |
  x-B-+   C
      |   |
      +---+
"""

# straight through intersections
test2 = """
  @
  | +-C--+
  A |    |
  +---B--+
    |      x
    |      |
    +---D--+
"""
## @|A+---B--+|+--C-+|-||+---D--+|x

fork_in_path = """
        x-B
          |
   @--A---+
          |
     x+   C
      |   |
      +---+
"""


multiple_starting_paths = """
  x-B-@-A-x
"""



upper_alpha = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


def create_map_arr(map_str):
    allowed = {'x', '@', '-', '|', '+', '\n', ' '}

    # check if map contains invalid characters
    for char in map_str:
        if char not in upper_alpha | allowed:
            raise ValueError('Map contains invalid characters:', char)

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

    # Find the dimensions of the map
    num_rows = len(map_list)
    num_cols = max(len(row) for row in map_list)
    # print(num_rows, num_cols)

    # pad rows with spaces if jagged
    for index, i in enumerate(map_list):
        if len(i) < num_cols:
            map_list[index] = f'{map_list[index]:<{num_cols}}'

    # convert strings to lists
    map_list = [list(i) for i in map_list]

    return map_list


# ========================================= TRAVERSE MAP LOGIC


def find_start(arr):
    for x, row in enumerate(arr):
        for y, char in enumerate(row):
            if char == '@':
                return x, y


def move(arr, pos, direction):
    x, y = pos
    if direction == 'left':
        next_pos = (x, y-1)
    elif direction == 'right':
        next_pos = (x, y+1)
    elif direction == 'up':
        next_pos = (x-1, y)
    elif direction == 'down':
        next_pos = (x+1, y)
    # else:
    #     raise ValueError(f"Invalid direction: {direction}")
    next_char = arr[next_pos[0]][next_pos[1]]
    if next_char in {'-', '|', '+', 'x'} | upper_alpha:
        return next_pos
    else:
        raise ValueError(f"Invalid move to position {next_pos}")



def traverse_map(map_arr):
    start_pos = find_start(map_arr)
    visited = set()
    stack = [start_pos]
    last_direction = None
    letters = []
    path = []

    while stack:
        pos = stack.pop()
        if pos in visited:
            continue
        visited.add(pos)
        path.append(map_arr[pos[0]][pos[1]])
        # todo even though we shouldnt go back to visited, we should still move over it in case of just passing thru
        directions = explore_directions(map_arr, pos)
        # todo if only true directions are those that have been visited already, set the append the one conforming to last direction to stack and continue
        # run_through_directions = {k: v for (k, v) in directions.items() if v['can_move'] and k == last_direction}
        # run_through_position = {direction: status.get('position') for direction, status in run_through_directions}.get(last_direction)
        # if run_through_position in visited:
        #     stack.append(run_through_position)
        #     continue


        # filter out already visited valid movements
        unvisited_directions = {k: v for (k, v) in directions.items() if v['position'] not in visited}
        num_directions = sum([direction['can_move'] for direction in unvisited_directions.values() if direction['can_move']])

        # if num_directions > 1 and pos != start_pos:
        #     raise ValueError('Fork in path!')
        if num_directions == 0:
            if map_arr[pos[0]][pos[1]] not in ['x', ' ', '|']:
                raise ValueError('Broken path!')
            return f'Congratulations! You\'ve reached the end of the map!\n {visited} \n {"".join(path)}'
        elif num_directions == 1:
            for direction, status in unvisited_directions.items():
                if status['can_move']:
                    next_pos = move(map_arr, pos, direction)
                    stack.append(next_pos)
                    last_direction = direction
        # contains intersection logic
        elif num_directions > 1:
            for direction, status in unvisited_directions.items():
                if status['can_move'] and direction == last_direction:
                    next_pos = move(map_arr, pos, direction)
                    stack.append(next_pos)
                    last_direction = direction

        # elif num_directions > 1 and pos == start_pos:
        #     for direction, status in unvisited_directions.items():
        #         if status['can_move']:
        #             next_pos = move(map_arr, pos, direction)
        #             stack.append(next_pos)
    return "".join(path)


def explore_directions(arr, pos):
    x, y = pos
    valid_movement = {'left': {'can_move': False, 'position': ()},
                      'right': {'can_move': False, 'position': ()},
                      'up': {'can_move': False, 'position': ()},
                      'down': {'can_move': False, 'position': ()}}
    # left
    if arr[x][y-1] in {'-', 'x', '+'} | upper_alpha and y != 0:
        valid_movement['left']['can_move'] = True
        valid_movement['left']['position'] = (x, y-1)

    # right
    if y != len(arr[0]) - 1 and arr[x][y+1] in {'-', 'x', '+'} | upper_alpha:
        valid_movement['right']['can_move'] = True
        valid_movement['right']['position'] = (x, y+1)

    # up
    if x != 0 and arr[x-1][y] in {'|', 'x', '+'} | upper_alpha:
        valid_movement['up']['can_move'] = True
        valid_movement['up']['position'] = (x-1, y)

    # down - guardian pattern in condition, TODO check for edge cases later
    if x < len(arr) - 1 and arr[x+1][y] in {'|', 'x', '+', '-'} | upper_alpha:
        valid_movement['down']['can_move'] = True
        valid_movement['down']['position'] = (x+1, y)

    return valid_movement


print(traverse_map(create_map_arr(test)))
# print(traverse_map(create_map_arr(multiple_starting_paths)))

