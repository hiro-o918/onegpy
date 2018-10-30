from gplib.terminator import terminator_checker


class TerminalCondition(object):
    def __init__(self, terminators=None):
        if terminators is None:
            terminators = []
        self._terminators = []

        for terminator in terminators:
            self.add(terminator)

    def add(self, terminator):
        terminator_checker(terminator)
        self._terminators.append(terminator)

    @property
    def terminators(self):
        return self._terminators

    def __call__(self):
        result = False
        for terminator in self._terminators:
            result = result or terminator()

        return not result

