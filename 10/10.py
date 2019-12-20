
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

def max_sight(asteroids):
    m = 0
    m_a = (0,0)
    for a in asteroids:
        ts = list(asteroids)
        ts.remove(a)
        c = 0
        for t in ts:
            vt = (t[0]-a[0], t[1]-a[1])
            dt = vt[0] * vt[0] + vt[1] * vt[1]
            bs = list(ts)
            bs.remove(t)
            blocked = False
            for b in bs:
                vb = (b[0] - a[0], b[1] - a[1])
                db = vb[0] * vb[0] + vb[1] * vb[1]
                dot = vb[0] * vt[0] + vb[1] * vt[1] 
                #if a == (4,2):
                #    print(f"From {a}, checking if {b} blocks {t}")
                #    print(f"vt {vt}, dt {dt}, vb, {vb}, db {db}, dot {dot}")
                if dt > db and dot > 0 and (dot * dot) == (db * dt):
                    blocked = True
                #    print(f"From {a}, {b} BLOCKS {t}")
                    break
            if not blocked:
                #print(f"From {a}, {t} is VISIBLE")
                c += 1
        #print(a, c)
        if c > m:
            m = c
            m_a = a
    print(m_a)
    print(m)
    return m

asts = parse_input("./input")
# print(asts)
max_sight(asts)