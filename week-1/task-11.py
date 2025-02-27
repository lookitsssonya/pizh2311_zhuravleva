from random import random

def ranrator(qty, minimum, maximum):
    while qty > 0:
        yield random() * (maximum - minimum) + minimum
        qty -= 1

a = ranrator(5, -2, 2)
for i in a:
    print(round(i, 2))