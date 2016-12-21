from itertools import combinations
from loader import load_file


def anycomb(items):
    ' return combinations of any length from the items '
    return ( comb
             for r in range(1, len(items) + 1)
             for comb in combinations(items, r)
    )


def totalvalue(comb):
    ' Totalise a particular combination of items'
    totwt = totval = 0
    for item, wt, val in comb:
        totwt += wt
        totval += val
    return (totval, -totwt) if totwt <= 400 else (0, 0)


capacity, items = load_file('input')


def fil(x):
    val, dummy = totalvalue(x)
    return val


def fil2(x):
    dummy, wt = totalvalue(x)
    return wt


xd = [x for x in anycomb(items) if -fil2(x) <= capacity]
bagged = max(xd, key=totalvalue)

print(bagged)
val, wt = totalvalue(bagged)
print '$', val, -wt, 'kg'