import pytest

from main import create_map_array, traverse_map, BrokenPathError, FakeTurnError, ForkInPathError, \
    MultipleStartingPathsError, InvalidPathError


def test_traverse_basic(basic_map):
    result_basic = traverse_map(create_map_array(basic_map))
    assert result_basic == ('ACB', '@---A---+|C|+---+|+-B-x')


def test_traverse_intersections(intersections_map):
    result_intersections = traverse_map((create_map_array(intersections_map)))
    assert result_intersections == ('ABCD', '@|A+---B--+|+--C-+|-||+---D--+|x')


def test_traverse_letters_as_turns(letters_as_turns_map):
    result_letters_turns = traverse_map(create_map_array(letters_as_turns_map))
    assert result_letters_turns == ('ACB', '@---A---+|||C---+|+-B-x')


def test_traverse_no_collect_twice(no_collect_twice_map):
    result_no_twice_collect = traverse_map(create_map_array(no_collect_twice_map))
    assert result_no_twice_collect == ('GOONIES', '@-G-O-+|+-+|O||+-O-N-+|I|+-+|+-I-+|ES|x')


def test_traverse_compact_space(compact_space_map):
    result_compact_space = traverse_map(create_map_array(compact_space_map))
    assert result_compact_space == ('BLAH', '@B+++B|+-L-+A+++A-+Hx')


def test_traverse_ignore_after_end(ignore_after_end_map):
    result_ignore_after_end = traverse_map(create_map_array(ignore_after_end_map))
    assert result_ignore_after_end == ('AB', '@-A--+|+-B--x')


def test_traverse_missing_start_raise(missing_start_map):
    with pytest.raises(InvalidPathError) as exc_info:
        traverse_map(create_map_array(missing_start_map))
    assert str(exc_info.value) == 'Missing start position "@" in map!'


def test_traverse_missing_end_raise(missing_end_map):
    with pytest.raises(InvalidPathError) as exc_info:
        traverse_map(create_map_array(missing_end_map))
    assert str(exc_info.value) == 'Missing end position "x" in map!'


def test_traverse_multiple_starts1_raise(multiple_starts_1_map):
    with pytest.raises(InvalidPathError) as exc_info:
        traverse_map(create_map_array(multiple_starts_1_map))
    assert str(exc_info.value) == 'Multiple start positions "@" in map!'


def test_traverse_multiple_starts_2_raise(multiple_starts_2_map):
    with pytest.raises(InvalidPathError) as exc_info:
        traverse_map(create_map_array(multiple_starts_2_map))
    assert str(exc_info.value) == 'Multiple start positions "@" in map!'


def test_traverse_multiple_starts_3_raise(multiple_starts_3_map):
    with pytest.raises(InvalidPathError) as exc_info:
        traverse_map(create_map_array(multiple_starts_3_map))
    assert str(exc_info.value) == 'Multiple start positions "@" in map!'


def test_traverse_fork_in_path_raise(fork_in_path_map):
    with pytest.raises(ForkInPathError) as exc_info:
        traverse_map(create_map_array(fork_in_path_map))
    assert str(exc_info.value) == 'Fork in path!'


def test_traverse_broken_path_raise(broken_path_map):
    with pytest.raises(BrokenPathError) as exc_info:
        traverse_map(create_map_array(broken_path_map))
    assert str(exc_info.value) == 'Broken path!'


def test_traverse_multiple_starting_paths_raise(multiple_starting_paths_map):
    with pytest.raises(MultipleStartingPathsError) as exc_info:
        traverse_map(create_map_array(multiple_starting_paths_map))
    assert str(exc_info.value) == 'Multiple starting paths!'


def test_traverse_fake_turn_raise(fake_turn_map):
    with pytest.raises(FakeTurnError) as exc_info:
        traverse_map(create_map_array(fake_turn_map))
    assert str(exc_info.value) == 'Fake turn!'
