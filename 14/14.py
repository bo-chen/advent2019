import math

class Reaction:
    output: str
    num_output: int
    inputs: {} # str : num

    def __init__(self, num, output):
        self.output = output
        self.num_output = num
        self.inputs = {}

    def __str__(self):
        out = f"{self.output} {self.num_output} <= {self.inputs}"
        return out

def parse_input(file):
    reactions = {}
    with open(file) as fp:
        for line in fp:
            [ins, o] = line.split(" => ")
            o = o.split(" ")
            r = Reaction(int(o[0]), o[1].strip())
            reactions[o[1].strip()] = r
            for i in ins.split(", "):
                ip = i.split(" ")
                r.inputs[ip[1].strip()] = int(ip[0])
            
    return reactions

def print_rs(rs):
    for (n, r) in rs.items():
        print(r)

def cost(rs, output, num_wanted, leftovers):
    if output == "ORE":
        return num_wanted

    left = leftovers.get(output)
    if left:
        if left >= num_wanted:
            leftovers[output] = left - num_wanted
            return 0
        else:
            num_wanted = num_wanted - left
            leftovers.pop(output)

    r = rs[output]
    repeats = math.ceil(num_wanted / r.num_output)

    c = 0
    for (o, n) in r.inputs.items():
        c += cost(rs, o, n * repeats, leftovers)

    leftovers[output] = r.num_output * repeats - num_wanted
    return c

rs = parse_input("./input")
leftovers = {}
max_unit_cost = 483766

produced = 0
ore_left = 1000000000000

while True:
    guess = int(ore_left / max_unit_cost)
    if guess == 0:
        guess = 1
    actual = cost(rs, "FUEL", guess, leftovers)
    ore_left -= actual
    if ore_left < 0:
        if guess == 1:
            break
        else:
            raise Exception("Unexpected overflow")
    produced += guess

print(produced)


# print(cost(rs, "FUEL", 1, {}))
