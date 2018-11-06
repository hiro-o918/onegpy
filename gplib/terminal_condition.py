from gplib.terminator import terminator_checker


class TerminalCondition(object):
    def __init__(self, terminators=None):
        """
        This class handles a set of terminators.

        :param terminators: list of Terminator
        """
        if terminators is None:
            terminators = []
        self._terminators = []

        for terminator in terminators:
            self.add(terminator)

    def add(self, terminator):
        """
        Add a terminator to an instance of condition.

        :param terminator: Terminator
        """
        terminator_checker(terminator)
        self._terminators.append(terminator)

    @property
    def terminators(self):
        return self._terminators

    def __call__(self):
        """
        If any one of terminators indicates `True`, return `True`.
        Otherwise returns False

        :return is_t_condition: bool.
        """
        is_t_condition = any([t() for t in self._terminators])

        return is_t_condition
