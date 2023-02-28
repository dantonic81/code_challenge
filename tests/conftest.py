import pytest


@pytest.fixture
def basic_map():
    return """
      @---A---+
              |
      x-B-+   C
          |   |
          +---+
    """


@pytest.fixture
def intersections_map():
    return """
      @
      | +-C--+
      A |    |
      +---B--+
        |      x
        |      |
        +---D--+
    """

@pytest.fixture
def letters_as_turns_map():
    return """
      @---A---+
              |
      x-B-+   |
          |   |
          +---C
    """


@pytest.fixture
def no_collect_twice_map():
    return """
         +-O-N-+
         |     |
         |   +-I-+
     @-G-O-+ | | |
         | | +-+ E
         +-+     S
                 |
                 x
    """


@pytest.fixture
def compact_space_map():
    return """
     +-L-+
     |  +A-+
    @B+ ++ H
     ++    x
    """


@pytest.fixture
def ignore_after_end_map():
    return """
      @-A--+
           |
           +-B--x-C--D
    """


@pytest.fixture
def missing_start_map():
    return """
         -A---+
              |
      x-B-+   C
          |   |
          +---+
    """


@pytest.fixture
def missing_end_map():
    return """
       @--A---+
                |
        B-+   C
          |   |
          +---+
    """


@pytest.fixture
def multiple_starts_1_map():
    return """
       @--A-@-+
                |
      x-B-+   C
          |   |
          +---+
    """


@pytest.fixture
def multiple_starts_2_map():
    return """
       @--A---+
                |
                C
                x
            @-B-+
    """


@pytest.fixture
def multiple_starts_3_map():
    return """
       @--A--x

      x-B-+
          |
          @
    """


@pytest.fixture
def fork_in_path_map():
    return """
            x-B
              |
       @--A---+
              |
         x+   C
          |   |
          +---+
    """


@pytest.fixture
def broken_path_map():
    return """
       @--A-+
             |

            B-x
    """


@pytest.fixture
def multiple_starting_paths_map():
    return """
      x-B-@-A-x
    """


@pytest.fixture
def fake_turn_map():
    return """
      @-A-+-B-x
    """
