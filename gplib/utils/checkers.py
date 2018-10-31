
def prob_checker(prob):
    if not 0 <= prob <= 1:
        typ = ValueError
        msg = 'prob must be in range [0, 1], but actual: {}'.format(prob)
    else:
        return

    raise typ(msg)
