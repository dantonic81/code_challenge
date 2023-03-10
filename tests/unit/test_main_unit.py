import pytest

from main import _get_valid_moves, _move, create_map_array, traverse_map
from utils.exceptions import InvalidMapError, InvalidDirectionError


def test_valid_map():
    map_str = 'A--\n|  \n@ x\n'
    expected_map_array = [['A', '-', '-'], ['|', ' ', ' '], ['@', ' ', 'x']]
    assert create_map_array(map_str) == expected_map_array


def test_invalid_map():
    with pytest.raises(InvalidMapError):
        traverse_map([])

    with pytest.raises(InvalidMapError):
        traverse_map([['x', 'y'], ['z']])


def test_move_left(basic_map):
    position = (1, 1)
    direction = 'left'
    expected_position = (1, 0)
    assert _move(basic_map, position, direction) == expected_position


def test_move_right(basic_map):
    position = (1, 1)
    direction = 'right'
    expected_position = (1, 2)
    assert _move(basic_map, position, direction) == expected_position


def test_move_up(basic_map):
    position = (1, 1)
    direction = 'up'
    expected_position = (0, 1)
    assert _move(basic_map, position, direction) == expected_position


def test_move_down(basic_map):
    position = (1, 1)
    direction = 'down'
    expected_position = (2, 1)
    assert _move(basic_map, position, direction) == expected_position


def test_get_valid_moves_left():
    map_array = [[' ', ' ', ' ', ' ', ' '],
                 [' ', '-', '-', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ']]
    position = (1, 2)
    expected_moves = {'left': {'can_move': True, 'position': (1, 1), 'character': '-'}}
    assert _get_valid_moves(map_array, position) == expected_moves


def test_get_valid_moves_right():
    map_array = [[' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', '-', '-', ' '],
                 [' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ']]
    position = (1, 2)
    expected_moves = {'right': {'can_move': True, 'position': (1, 3), 'character': '-'}}
    assert _get_valid_moves(map_array, position) == expected_moves


def test_get_valid_moves_up():
    map_array = [[' ', ' ', '+', ' ', ' '],
                 [' ', ' ', '|', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ']]
    position = (1, 2)
    expected_moves = {'up': {'can_move': True, 'position': (0, 2), 'character': '+'}}
    assert _get_valid_moves(map_array, position) == expected_moves


def test_get_valid_moves_down():
    map_array = [[' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', '|', ' ', ' '],
                 [' ', ' ', '|', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ']]
    position = (1, 2)
    expected_moves = {'down': {'can_move': True, 'position': (2, 2), 'character': '|'}}
    assert _get_valid_moves(map_array, position) == expected_moves


def test_get_valid_moves_no_valid_moves():
    map_array = [[' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', '-', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ']]
    position = (1, 2)
    expected_moves = {}
    assert _get_valid_moves(map_array, position) == expected_moves


def test_get_valid_moves_edge_case():
    map_array = [['A']]
    position = (0, 0)
    expected_moves = {}
    assert _get_valid_moves(map_array, position) == expected_moves


def test_move_invalid_direction_raise(basic_map):
    position = (1, 1)
    direction = 'invalid'
    with pytest.raises(InvalidDirectionError) as exc_info:
        _move(basic_map, position, direction)
    assert str(exc_info.value) == f"Direction '{direction}' not allowed!"