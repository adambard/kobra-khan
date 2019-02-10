from collections import defaultdict

def frequencies(xs):
    ret = defaultdict(lambda: 0)
    while xs:
        x, *xs = xs
        ret[x] += 1

    return ret

