from gplib.operator import operator_checker


class Sequential(object):
    def __init__(self, operators=None):
        if operators is None:
            operators = []
        self._operators = []

        for operator in operators:
            self.add(operator)

    def add(self, operator):
        self._added_operator_checker(operator)
        self._operators.append(operator)

    @property
    def operators(self):
        return self._operators

    def _added_operator_checker(self, operator):
        operator_checker(operator)

        if (self._operators and operator.n_in is not None) \
                and self._operators[-1].n_out != operator.n_in:
            msg = 'Invalid operator:\n' \
                  'Expected operator.n_in: {} {} None not {}' \
                .format(self._operators[-1].n_out or '',
                        'or' if self._operators[-1].n_out is not None else '',
                        operator.n_in)

            raise TypeError(msg)

    def __call__(self, population):
        out = population
        for operator in self._operators:
            # if `operator` is  destructive, it perhaps returns None
            out = operator(out) or out

        return out

