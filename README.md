# Code_challenge - Map Traverser
This module provides a set of functions to traverse a rectangular map represented as a 2D list of characters. 
I've chosen the depth-first search (DFS) algorithm because it uses less memory and is more appropriate for our use case where
path finding is needed. For this purpose there's an interplay between stack and visited list in the traverse_map function that we must stick to unless we want to use a different algorithm e.g. breadth-first search (BFS). 

The map should contain only the following characters:

- uppercase letters ('A' to 'Z')
- special characters ('x', '@', '-', '|', '+', '\n', ' ') representing the start, end, corners, empty spaces etc.

The **create_map_array(map_str)** function can be used to convert a string representation of the map to a 2D list of characters.

## Functions

### **create_map_array(map_str) -> List[List[str]]**

This function converts a string representation of the map to a 2D list of characters. The input string should contain only the allowed characters mentioned above, and the function will raise an **InvalidMapError** if the input string contains any other characters.

The input string should contain exactly one '@' character representing the starting position, and one or more 'x' characters representing the ending position. The function will raise an **InvalidMapError** if either of these characters is missing or if there are multiple '@' characters in the input string.

The function will pad the rows of the 2D list with spaces to make all rows have the same length, and return a rectangular map where each character corresponds to one cell in the grid.

**Parameters:**

- **map_str** (str): a string representation of a map

**Returns**:

- A 2D list of characters representing the map

**Raises**:

- **InvalidMapError**: if the input string contains any invalid character or if the '@' or 'x' character(s) are missing or not unique in the input string.

### traverse_map(map_array: List[List[str]]) -> Tuple[str, str]

This function traverses the rectangular map represented as a 2D list of characters and returns the collected letters and path.

**Parameters**:

- **map_array** (List[List[str]]): A list of lists representing the map.

**Returns**:

- A tuple containing the collected letters and path. 

## Internal functions

The following functions are used by the **traverse_map** function, but are not intended to be used outside of this module.

### **_find_start(map_array: List[List[str]]) -> Tuple[int, int]**

This function finds the starting position in the given 2D list of characters representing the map.

**Parameters**:

- **map_array** (List[List[str]]): A list of lists representing the map.

**Returns**:

- A tuple containing the starting position coordinates (row, col).

**Raises**:

- **InvalidMapError**: if the starting position is not found in the map.

### **_move(map_array: List[List[str]], position: Tuple[int, int], direction: str) -> Tuple[int, int]**

This function takes the current position, and a direction to move (up, down, left or right) and returns the new position after the move. The function will raise an **InvalidDirectionError** if the direction is invalid.

**Parameters**:

- **map_array** (List[List[str]]): A list of lists representing the map.
- **position** (Tuple[int, int]): A tuple containing the current position coordinates (row, col).
- **direction** (str): The direction to move, one of ('up', 'down', 'left', 'right').

**Returns**:

- A tuple containing the new position coordinates (row, col).

**Raises**:

- **InvalidDirectionError**: if the direction is invalid.

### **_get_valid_moves(map_array: List[List[str]], position: Tuple[int, int]) -> Dict[str, Dict[str, object]]**

This function returns a dictionary containing the valid moves from the current position in the given 2D list of characters representing the map

## Tests

Tests are organized into their respective unit and acceptance packages with **conftest.py** file containing fixtures.

The test cases are written using the **pytest** library and include both basic and edge cases to ensure the functionality and correctness of the **traverse_map** function.

### Acceptance test cases

- **test_traverse_basic**: This test case checks if the traverse_map function can correctly traverse a basic map.

- **test_traverse_intersections**: This test case checks if the traverse_map function can correctly traverse a map with intersections.

- **test_traverse_letters_as_turns**: This test case checks if the traverse_map function can correctly traverse a map with letters as turns.

- **test_traverse_no_collect_twice**: This test case checks if the traverse_map function can correctly traverse a map where letters can only be collected once.

- **test_traverse_compact_space**: This test case checks if the traverse_map function can correctly traverse a map with a compact space.

- **test_traverse_ignore_after_end**: This test case checks if the traverse_map function can correctly traverse a map where everything after the end point is ignored.

- **test_traverse_missing_start_raise**: This test case checks if the **traverse_map** function raises an InvalidMapError when the map is missing the start position.

- **test_traverse_missing_end_raise**: This test case checks if the **traverse_map** function raises an InvalidMapError when the map is missing the end position.

- **test_traverse_multiple_starts1_raise**: This test case checks if the **traverse_map** function raises an InvalidMapError when the map has multiple start positions.

- **test_traverse_multiple_starts_2_raise**: This test case checks if the **traverse_map** function raises an InvalidMapError when the map has multiple start positions.

- **test_traverse_multiple_starts_3_raise**: This test case checks if the **traverse_map** function raises an InvalidMapError when the map has multiple start positions.

- **test_traverse_fork_in_path_raise**: This test case checks if the **traverse_map** function raises a ForkInPathError when the map has a fork in the path.

- **test_traverse_broken_path_raise**: This test case checks if the **traverse_map** function raises a BrokenPathError when the map has a broken path.

- **test_traverse_multiple_starting_paths_raise**: This test case checks if the **traverse_map** function raises a MultipleStartingPathsError when the map has multiple starting paths.

- **test_traverse_fake_turn_raise**: This test case checks if the **traverse_map** function raises a FakeTurnError when the map has a fake turn.

### Unit test cases

- **test_valid_map**: This test case checks whether the **create_map_array** function correctly converts a given map string to a 2D array. It asserts whether the output of the function matches the expected output.

- **test_invalid_map**: This test case checks whether the **traverse_map** function raises an **InvalidMapError** exception when passed an empty list or a list with an invalid map. It asserts that the exceptions are raised as expected.

- **test_move_left**: This test case checks whether the **_move** function moves the player one step to the left on a basic map. It asserts whether the output of the function matches the expected position.

- **test_move_right**: This test case checks whether the **_move** function moves the player one step to the right on a basic map. It asserts whether the output of the function matches the expected position.

- **test_move_up**: This test case checks whether the **_move** function moves the player one step up on a basic map. It asserts whether the output of the function matches the expected position.

- **test_move_down**: This test case checks whether the **_move** function moves the player one step down on a basic map. It asserts whether the output of the function matches the expected position.

- **test_get_valid_moves_left**: This test case checks whether the **_get_valid_moves** function returns a dictionary with the expected information when the player is at a position where they can move left. It asserts whether the output of the function matches the expected dictionary.

- **test_get_valid_moves_right**: This test case checks whether the **_get_valid_moves** function returns a dictionary with the expected information when the player is at a position where they can move right. It asserts whether the output of the function matches the expected dictionary.

- **test_get_valid_moves_up**: This test case checks whether the **_get_valid_moves** function returns a dictionary with the expected information when the player is at a position where they can move up. It asserts whether the output of the function matches the expected dictionary.

- **test_get_valid_moves_down**: This test case checks whether the **_get_valid_moves** function returns a dictionary with the expected information when the player is at a position where they can move down. It asserts whether the output of the function matches the expected dictionary.

- **test_get_valid_moves_no_valid_moves**: This test case checks whether the **_get_valid_moves** function returns an empty dictionary when there are no valid moves from the current position. It asserts whether the output of the function matches the expected empty dictionary.

- **test_get_valid_moves_edge_case**: This test case checks whether the **_get_valid_moves** function returns an empty dictionary when the map is of size 1x1 and the player is at that position. It asserts whether the output of the function matches the expected empty dictionary.

- **test_move_invalid_direction_raise**: This test case checks whether the **_move** function raises an **InvalidDirectionError** exception when passed an invalid direction. It asserts that the exception message matches the expected string.

## Exceptions

The code also includes several custom exception classes from the **exceptions** module. These classes are used to handle specific errors that may occur during the traversal of a map.

- **BrokenPathError**: Raised when the map has a broken path.

- **FakeTurnError**: Raised when the map has a fake turn.

- **ForkInPathError**: Raised when the map has a fork in the path.

- **InvalidMapError**: Raised when the map is invalid.

- **MultipleStartingPathsError**: Raised when the map has multiple starting paths.

## Dependencies
This project has the following dependencies:

- **pytest**: A testing framework used to write and run tests.
- **main**: A Python module containing the create_map_array and traverse_map functions.
- **utils.exceptions**: A Python module containing custom exception classes