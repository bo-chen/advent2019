
class Node:
    name: str
    parent = None
    children: list = []
    def __init__(self):
        self.children = []

class State:
    nodes: dict
    def __init__(self):
        self.nodes = {}


def parse_input(file):
    s = State()
    # Add root first
    s.nodes["COM"] = Node()
    s.nodes["COM"].name = "COM"

    with open(file) as fp:
        for line in fp:
            args = line.split(")")
            if len(args) != 2:
                raise Exception("Unexpected line", line)
            new = Node()
            new.name = args[1].strip()
            new.parent = args[0]
            s.nodes[new.name] = new

    # Fix up child relationships
    for n in s.nodes.values():
        if n.name != "COM":
            s.nodes[n.parent].children.append(n.name)
    
    return s

def depth(s, n):
    if n.name == "COM":
        return 0
    return 1 + depth(s, s.nodes[n.parent])

def checksum(s): 
    t = 0
    for n in s.nodes.values():
        t += depth(s, n)
    return t       

def bfs(s):
    queue = [(s.nodes["YOU"],0)]
    checked = {}

    while True:
        if len(queue) == 0:
            return

        (n, d) = queue.pop(0)
        print(n.name, d)
        print(n.parent, n.children)
        print("")
        if n.name == "SAN":
            return d
        
        if n.name != "COM" and checked.get(n.parent) == None:
            checked[n.parent] = True
            queue.append((s.nodes[n.parent], d + 1))
        
        for c in n.children:
            if checked.get(c) == None:
                checked[c] = True
                queue.append((s.nodes[c], d + 1))

s = parse_input("./s1")
# - 2 to not count you and santa as orbits
print(bfs(s) - 2)