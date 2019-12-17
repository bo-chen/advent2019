import sys
import os

def calc_fuel(weight):
    f = int(weight / 3) - 2
    if f > 0:
        return f + calc_fuel(f)
    elif f < 0:
        return 0
    else: 
        return f

total = 0
with open("./input.txt") as fp:
    for line in fp:
        i = int(line)
        total += calc_fuel(i)

print(total)


   