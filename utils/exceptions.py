class InvalidMapError(Exception):
    pass


class BrokenPathError(InvalidMapError):
    pass


class FakeTurnError(InvalidMapError):
    pass


class ForkInPathError(InvalidMapError):
    pass


class MultipleStartingPathsError(InvalidMapError):
    pass
