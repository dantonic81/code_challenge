import pytest

from test3 import create_map_arr, traverse_map

# basic example  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
basic = """
  @---A---+
          |
  x-B-+   C
      |   |
      +---+
"""

# straight through intersections  ----------------------------------------------------------------
intersections = """
  @
  | +-C--+
  A |    |
  +---B--+
    |      x
    |      |
    +---D--+
"""
# expected ABCD  actual: abc
# expected  @|A+---B--+|+--C-+|-||+---D--+|x actual: @|A+---B--+|+--C-+|
# probably the toughest issue on which at least two other tasks depend
# if its not an intersection, we should just continue movement


# letters may be found on turns    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
letters_turns = """
  @---A---+
          |
  x-B-+   |
      |   |
      +---C
"""

# no twice collect   ------------------------------------------------------------
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
# expected  GOONIES    actual: GO
# expected  @-G-O-+|+-+|O||+-O-N-+|I|+-+|+-I-+|ES|x   actual: @-G-O-+|+-+|
# looks like waiting for intersections to be resolved


# compact_space    -------------------------------------------------------------
compact_space = """
 +-L-+
 |  +A-+
@B+ ++ H
 ++    x
"""
# expected: BLAH                           actual: broken path   actual: @B+++
# expected: @B+++B|+-L-+A+++A-+Hx
# looks like waiting for intersections to be resolved

# ignore_after_end  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ignore_after_end = """
  @-A--+
       |
       +-B--x-C--D
"""

# expected: AB                   actual: AB
# expected: @-A--+|+-B--x        actual: @-A--+|+-B--x


# ###################################### invalid maps ##############################################


#  missing_start ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
missing_start = """
     -A---+
          |
  x-B-+   C
      |   |
      +---+
"""

# missing_end +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
missing_end = """
   @--A---+
          |
    B-+   C
      |   |
      +---+
"""

# multiple_starts1   ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
multiple_starts1 = """
   @--A-@-+
          |
  x-B-+   C
      |   |
      +---+
"""

# multiple_starts2  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
multiple_starts2 = """
   @--A---+
          |
          C
          x
      @-B-+
"""

# multiple_starts3  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
multiple_starts3 = """
   @--A--x

  x-B-+
      |
      @
"""

# fork_in_path     +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
fork_in_path = """
        x-B
          |
   @--A---+
          |
     x+   C
      |   |
      +---+
"""

# actual: @--A---+


# broken_path    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
broken_path = """
   @--A-+
        |
         
        B-x
"""

# multiple_starting_paths  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
multiple_starting_paths = """
  x-B-@-A-x
"""
# actual:  @

# fake turn   +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
fake_turn = """
  @-A-+-B-x
"""


def test_basic():
    result_basic = traverse_map(create_map_arr(basic))
    assert result_basic == ('ACB', '@---A---+|C|+---+|+-B-x')


def test_intersections():
    result_intersections = traverse_map((create_map_arr(intersections)))
    assert result_intersections == 1


def test_letters_turns():
    result_letters_turns = traverse_map(create_map_arr(letters_turns))
    assert result_letters_turns == ('ACB', '@---A---+|||C---+|+-B-x')


def test_no_twice_collect():
    result_no_twice_collect = traverse_map(create_map_arr(no_twice_collect))
    assert result_no_twice_collect == 1


def test_compact_space():
    result_compact_space = traverse_map(create_map_arr(compact_space))
    assert result_compact_space == 1


def test_ignore_after_end():
    result_ignore_after_end = traverse_map(create_map_arr(ignore_after_end))
    assert result_ignore_after_end == ('AB', '@-A--+|+-B--x')


def test_missing_start_raise():
    with pytest.raises(ValueError) as exc_info:
        traverse_map(create_map_arr(missing_start))
    assert str(exc_info.value) == 'Map has no start!'


def test_missing_end_raise():
    with pytest.raises(ValueError) as exc_info:
        traverse_map(create_map_arr(missing_end))
    assert str(exc_info.value) == 'Map has no end!'


def test_multiple_starts1_raise():
    with pytest.raises(ValueError) as exc_info:
        traverse_map(create_map_arr(multiple_starts1))
    assert str(exc_info.value) == 'Map has multiple starts!'


def test_multiple_starts2_raise():
    with pytest.raises(ValueError) as exc_info:
        traverse_map(create_map_arr(multiple_starts2))
    assert str(exc_info.value) == 'Map has multiple starts!'


def test_multiple_starts3_raise():
    with pytest.raises(ValueError) as exc_info:
        traverse_map(create_map_arr(multiple_starts3))
    assert str(exc_info.value) == 'Map has multiple starts!'


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


# broken_path             +

# program
# [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', '@', '-', '-', 'A', '-', '+', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', '-', 'x', ' ']]

# pdb
# [[' ', ' ', ' ', '@', '-', '-', 'A', '-', '+', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', '-', 'x']]

"""
   @--A-+
        |
         
        B-x
"""