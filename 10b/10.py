
import math

# Returns list of asteroid coordinates
def parse_input(file):
    y = 0
    x = 0
    asteroids = []
    with open(file) as fp:
        for line in fp:
            x = 0
            for c in line:
                if c == "#":
                    asteroids.append((x,y))
                x += 1
            y += 1
    return asteroids

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] 

def lucky_200(asteroids, a):
    ts = list(asteroids)
    ts.remove(a)
    angles = {}
    for t in ts:
        vt = (t[0]-a[0], t[1]-a[1])
        up = (0, -1)
        dt = dot(vt,vt)
        dott = dot(vt, up)
        # really cos(angle)^2
        angle = dott * dott / dt
        # fixup from quadrant
        if dott < 0:
            angle = angle * -1
        if vt[0] >= 0:
            angle = 1 - angle
        else:
            angle = 3 + angle
        if angles.get(angle):
            angles[angle].append(t)
        else:
            angles[angle] = [t]

    print(angles)
    all_as = list(sorted(angles.keys()))
    print(len(all_as))

    the_angle = all_as[199]
    line = angles[the_angle]
    print(line)
    print(list(sorted(line,key =(lambda t: (t[0]-a[0]) * (t[0]-a[0]) + (t[1]-a[1]) * (t[1] - a[1])))))

    return 

asts = parse_input("./input")
# should be at (11, 19) 253
a = (11,19)
lucky_200(asts, a)