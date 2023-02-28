import pytest

from main import create_map_arr, traverse_map

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


def test_basic():
    result_basic = traverse_map(create_map_arr(basic))
    assert result_basic == ('ACB', '@---A---+|C|+---+|+-B-x')


def test_intersections():
    result_intersections = traverse_map((create_map_arr(intersections)))
    assert result_intersections == ('ABCD', '@|A+---B--+|+--C-+|-||+---D--+|x')


def test_letters_turns():
    result_letters_turns = traverse_map(create_map_arr(letters_turns))
    assert result_letters_turns == ('ACB', '@---A---+|||C---+|+-B-x')


def test_no_twice_collect():
    result_no_twice_collect = traverse_map(create_map_arr(no_twice_collect))
    assert result_no_twice_collect == ('GOONIES', '@-G-O-+|+-+|O||+-O-N-+|I|+-+|+-I-+|ES|x')


def test_compact_space():
    result_compact_space = traverse_map(create_map_arr(compact_space))
    assert result_compact_space == ('BLAH', '@B+++B|+-L-+A+++A-+Hx')


def test_ignore_after_end():
    result_ignore_after_end = traverse_map(create_map_arr(ignore_after_end))
    assert result_ignore_after_end == ('AB', '@-A--+|+-B--x')


def test_missing_start_raise():
    with pytest.raises(ValueError) as exc_info:
        traverse_map(create_map_arr(missing_start))
    assert str(exc_info.value) == 'Missing start position "@" in map!'


def test_missing_end_raise():
    with pytest.raises(ValueError) as exc_info:
        traverse_map(create_map_arr(missing_end))
    assert str(exc_info.value) == 'Missing end position "x" in map!'


def test_multiple_starts1_raise():
    with pytest.raises(ValueError) as exc_info:
        traverse_map(create_map_arr(multiple_starts1))
    assert str(exc_info.value) == 'Multiple start positions "@" in map!'


def test_multiple_starts2_raise():
    with pytest.raises(ValueError) as exc_info:
        traverse_map(create_map_arr(multiple_starts2))
    assert str(exc_info.value) == 'Multiple start positions "@" in map!'


def test_multiple_starts3_raise():
    with pytest.raises(ValueError) as exc_info:
        traverse_map(create_map_arr(multiple_starts3))
    assert str(exc_info.value) == 'Multiple start positions "@" in map!'


def test_fork_in_path_raise():
    with pytest.raises(ValueError) as exc_info:
        traverse_map(create_map_arr(fork_in_path))
    assert str(exc_info.value) == 'Fork in path!'


def test_broken_path_raise():
    with pytest.raises(ValueError) as exc_info:
        traverse_map(create_map_arr(broken_path))
    assert str(exc_info.value) == 'Broken path!'


def test_multiple_starting_paths_raise():
    with pytest.raises(ValueError) as exc_info:
        traverse_map(create_map_arr(multiple_starting_paths))
    assert str(exc_info.value) == 'Multiple starting paths!'


def test_fake_turn_raise():
    with pytest.raises(ValueError) as exc_info:
        traverse_map(create_map_arr(fake_turn))
    assert str(exc_info.value) == 'Fake turn!'
