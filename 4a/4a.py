import os
import sys

def check(n):
    s = str(n)
    prev = s[0]
    double_progress = False
    double_locked = False
    double_broken = False
    for c in s[1:]:
        if int(c) < int(prev):
            return False
        if double_progress:
            if c == prev:
                double_broken = True
            else:
                double_progress = False
                if not double_broken:
                    double_locked = True
        elif c == prev:
            double_broken = False
            double_progress = True
        prev = c
    return double_locked or (double_progress and not double_broken)

def count_nums(min, max):
    count = 0
    for n in range(min, max):
        if check(n):
            count +=1
    return count

