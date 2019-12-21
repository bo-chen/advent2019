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

def step(ps, vs):
    num = len(ps)
    # gravity
    for o in range(num):
        for n in range(num):
            if o == n:
                # actually should not have effect
                continue
            for d in range(3):
                if ps[o][d] < ps[n][d]:
                    vs[o][d] += 1
                elif ps[o][d] > ps[n][d]:
                    vs[o][d] -= 1
    
    # move
    for o in range(num):
        for d in range(3):
            ps[o][d] += vs[o][d]


ps = parse_input("./input")
vs = []
for _ in ps:
    vs.append([0,0,0])
for i in range(1000):
    step(ps,vs)
    #print(f"PS= {ps}")
    #print(f"VS= {vs}")
    #print("")
t = 0
for n in range(len(ps)):
    t += sum(map(lambda x: abs(x), ps[n])) * sum(map(lambda x: abs(x), vs[n]))
print(ps)
print(vs)
print(t)
