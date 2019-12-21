import math

def parse_input(file):
    ps = []
    with open(file) as fp:
        for line in fp:
            comps = line.split(",")
            ps.append([
                int(comps[0].split("=")[1]),
                int(comps[1].split("=")[1]),
                int(comps[2].split("=")[1].split(">")[0]) 
                ])
    return ps

# step just one dimension
def step_d(ps, vs, d):
    num = len(ps)
    # gravity
    for o in range(num):
        for n in range(num):
            if o == n:
                # actually should not have effect
                continue
            for d in [d]:
                if ps[o][d] < ps[n][d]:
                    vs[o][d] += 1
                elif ps[o][d] > ps[n][d]:
                    vs[o][d] -= 1
    
    # move
    for o in range(num):
        for d in [d]:
            ps[o][d] += vs[o][d]


ps = parse_input("./input")
vs = []
t = 1
for _ in ps:
    vs.append([0,0,0])

for d in range(3):
    i = 0
    while True:
        i += 1
        step_d(ps,vs,d)
        # Velociy is 0 at the harmonics
        if vs[0][d] == 0 and vs[1][d] == 0 and vs[2][d] == 0 and vs[3][d] == 0:
            print(f"Dimension {d} repeated in {i} steps")
            t = t * i
            break

print(t)