class InvalidPathError(Exception):
    pass


class BrokenPathError(InvalidPathError):
    pass


class FakeTurnError(InvalidPathError):
    pass


class ForkInPathError(InvalidPathError):
    pass


class MultipleStartingPathsError(InvalidPathError):
    pass
