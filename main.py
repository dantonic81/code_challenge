basic = """
  @---A---+
          |
  x-B-+   C
      |   |
      +---+
"""

intersections = """
  @
  | +-C--+
  A |    |
  +---B--+
    |      x
    |      |
    +---D--+
"""

letters_turns = """
  @---A---+
          |
  x-B-+   |
      |   |
      +---C
"""

no_twice_collect = """
     +-O-N-+
     |     |
     |   +-I-+
 @-G-O-+ | | |
     | | +-+ E
     +-+     S
             |
             x
"""

compact_space = """  
 +-L-+
 |  +A-+
@B+ ++ H
 ++    x
"""

ignore_after_end = """ 
  @-A--+
       |
       +-B--x-C--D
"""

# ###################################### invalid maps ##############################################


missing_start = """      
     -A---+
          |
  x-B-+   C
      |   |
      +---+
"""

missing_end = """
   @--A---+
          |
    B-+   C
      |   |
      +---+
"""

multiple_starts1 = """
   @--A-@-+
          |
  x-B-+   C
      |   |
      +---+
"""

multiple_starts2 = """
   @--A---+
          |
          C
          x
      @-B-+
"""

multiple_starts3 = """
   @--A--x

  x-B-+
      |
      @
"""

fork_in_path = """     
        x-B
          |
   @--A---+
          |
     x+   C
      |   |
      +---+
"""

broken_path = """
   @--A-+
        |

        B-x
"""

multiple_starting_paths = """
  x-B-@-A-x
"""

fake_turn = """
  @-A-+-B-x
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

    # Find the number of columns, number of rows is not needed for padding
    num_cols = max(len(row) for row in map_list)

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
        raise ValueError(f"Invalid move to position {next_pos}")


def traverse_map(map_arr):
    start_pos = find_start(map_arr)
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
            return "".join(letters), "".join(path)

        if current_pos in upper_alpha and pos not in locations_picked:
            letters.append(current_pos)
            locations_picked.append(pos)
        directions = explore_directions(map_arr, pos)

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
                    next_pos = move(map_arr, pos, direction)
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
                    next_pos = move(map_arr, pos, direction)
                    stack.append(next_pos)
                    last_direction = direction

    return "".join(path)


def explore_directions(arr, pos):
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


print(traverse_map(create_map_arr(intersections)))
# print(traverse_map(create_map_arr(multiple_starting_paths)))
# print(create_map_arr(broken_path))

