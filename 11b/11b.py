DEBUG = False

class State:
    instruction_counter: int
    mem: list
    inputs: list
    outputs: list
    signal: str
    relative_base: int

    def __init__(self, mem: list, instruction_counter: int=0):
        self.instruction_counter = 0
        self.mem = mem
        self.instruction_counter = instruction_counter
        self.inputs = []
        self.outputs = []
        self.signal = None
        self.relative_base = 0

    def __str__(self):
        i = 0
        out = "STATE:\n"
        if DEBUG:
            for n in range(0,10):
                out += f"\t{n}"
            out += f"\n-----------------------------------------------------------------------------------\n"
            while (i < len(self.mem)):
                if (i == self.instruction_counter):
                    out += f"\t|{self.mem[i]}|"
                else:
                    out += f"\t{self.mem[i]}"
                i += 1
                if (i % 10 == 0):
                    out += f"\n{i}"
            out += "\n"
        out += f"instruction_counter: {self.instruction_counter}, relative_base: {self.relative_base}\n" 
        out += f"inputs: {self.inputs}, outputs: {self.outputs}\n"
        out += f"signal: {self.signal}, \n"
        return out

# Reads initial state of the program 
def parse_input(file):
    with open(file) as fp:
        a = []
        for line in fp:
            a += line.split(",")
    return list(map(lambda s: int(s), a))

OPCFG = {
    1  : {"op" : "ADD", "size" : 4}, 
    2  : {"op" : "MUL", "size" : 4},
    3  : {"op" : "IN" , "size" : 2},
    4  : {"op" : "OUT", "size" : 2},
    5  : {"op" : "JPT", "size" : 3},
    6  : {"op" : "JPF", "size" : 3},
    7  : {"op" : "LT" , "size" : 4},
    8  : {"op" : "EQ" , "size" : 4},
    9  : {"op" : "SRB", "size" : 2},
    99 : {"op" : "HALT", "size" : 1}
    }

class Instruction:
    original: str
    size: int
    op: str
    args: list
    argmodes: list

    def __str__(self):
        return f"(op:{self.op}, size:{self.size}, args:{self.args}, argmodes:{self.argmodes}, original:{self.original})"

    def __init__(self, ins: list):
        self.original = ins
        opcfg = OPCFG[ins[0] % 100]
        self.op = opcfg["op"]
        self.size = opcfg["size"]

        if len(ins) < self.size:
            raise Exception(f"Wrong size instruction {str(ins)}")

        self.args = ins[1:self.size]
        self.argmodes = list(reversed(str(ins[0] // 100)))
        # pad 0s
        self.argmodes.extend(["0"] * (self.size - 1 - len(self.argmodes)) )

    def savearg(self, state : State, pos : int, val : int):
        addr = -1
        if self.argmodes[pos] == "0":
            addr = self.args[pos]
        elif self.argmodes[pos] == "2":
            addr = self.args[pos] + state.relative_base
        else:
            raise Exception("Wrong argmode to save", self)
        
        if addr < 0:
            raise Exception("Negative address")
        if addr >= len(state.mem):
            # simple memory increase heuristic
            state.mem.extend([0] * addr)
        state.mem[addr] = val

    def loadarg(self, state : State, pos : int):
        mode = self.argmodes[pos]
        # Immediate
        if mode == "1":
            return self.args[pos]
        # Addressed modes
        elif mode == "0":
            addr = self.args[pos]
        elif mode == "2":
            addr = self.args[pos] + state.relative_base
        else:
            raise Exception("Unknown argmode", str(self))
        if addr < 0:
            raise Exception("Negative address")
        if addr >= len(state.mem):
            return 0
        return state.mem[addr]

# Execute next instruction, return true if HALT
def execute_next(state : State):  
    ins = Instruction(state.mem[state.instruction_counter : state.instruction_counter + 4])
    if DEBUG:
        print(ins)

    # normal instructions
    if ins.op == "ADD":
        ins.savearg(state, 2, ins.loadarg(state, 0) + ins.loadarg(state, 1))
    elif ins.op == "MUL":
        ins.savearg(state, 2, ins.loadarg(state, 0) * ins.loadarg(state, 1))
    elif ins.op == "IN":
        if not state.inputs:
            # Interrupt and wait for input before continuing
            state.signal = "IN"
            return state.signal
        else:
            ins.savearg(state, 0, state.inputs.pop(0))
    elif ins.op == "OUT":
        state.outputs.append(ins.loadarg(state, 0))
        state.signal = "OUT"
        # Interrupt for output, but consider instruction as successful and increment counter
        state.instruction_counter += ins.size
        return state.signal
    elif ins.op == "HALT":
        state.signal = "HALT"
        return state.signal
    # jump instructions
    elif ins.op == "JPT":
        if ins.loadarg(state, 0) != 0:
            state.instruction_counter = ins.loadarg(state, 1)
            return None
    elif ins.op == "JPF":
        if ins.loadarg(state, 0) == 0:
            state.instruction_counter = ins.loadarg(state, 1)
            return None
    elif ins.op == "LT":
        if ins.loadarg(state, 0) < ins.loadarg(state, 1):
            ins.savearg(state, 2, 1)
        else:
            ins.savearg(state, 2, 0)
    elif ins.op == "EQ":
        if ins.loadarg(state, 0) == ins.loadarg(state, 1):
            ins.savearg(state, 2, 1)
        else:
            ins.savearg(state, 2, 0)
    elif ins.op == "SRB":
        state.relative_base += ins.loadarg(state, 0)

    state.instruction_counter += ins.size
    return state.signal

def execute_all(state : State):
    state.signal = None
    if DEBUG:
        print("START EXECUTION")
        print(state)

    while True:
        signal = execute_next(state)
        if DEBUG:
            print(state)
        if signal:
            break

    if DEBUG:
        print("END EXECUTION")
    
    return signal

class Robot:
    pos: tuple
    d: list
    painted: dict

    def __init__(self):
        self.pos = (0,0)
        # Use the first element to indicate current direction
        self.d = ["U","R","D","L"]
        self.painted = {}
    
    def get_input(self):
        c = self.painted.get(self.pos)
        if c:
            return c 
        else: 
            return 0
    
    def paint(self, val):
        self.painted[self.pos] = val

    def turn_and_move(self, r):
        if r == 0:
            # left
            self.d = self.d[-1:] + self.d[:-1]
        elif r == 1:
            # right
            self.d = self.d[1:] + self.d[:1]
        else:
            raise Exception("Illegal turn", r)

        # Now move
        if self.d[0] == "U":
            self.pos = (self.pos[0], self.pos[1] + 1)
        elif self.d[0] == "R":
            self.pos = (self.pos[0] + 1, self.pos[1])
        elif self.d[0] == "D":
            self.pos = (self.pos[0], self.pos[1] - 1)
        elif self.d[0] == "L":
            self.pos = (self.pos[0] - 1, self.pos[1])
        else:
            raise Exception("Facing illegal direction", self.d)

def print_canvas(ps):
    ordered = list(sorted(ps.items(), key=lambda p: p[0][1] * -10000000 + p[0][0]))
    prev = ordered.pop(0)
    print("  " * prev[0][0], end="")
    print("XX" if prev[1] == 1 else "  ", end="")
    for p in ordered:
        if p[0][1] < prev[0][1]:
            print("\n" * (prev[0][1] - p[0][1]), end="")
            print("  " * p[0][0], end="")
            print("XX" if p[1] == 1 else "  ", end="")
        elif p[0][1] > prev[0][1]:
            raise Exception("wrong sort order")
        else:
            print("  " * (p[0][0] - prev[0][0] - 1), end="")
            print("XX" if p[1] == 1 else "  ", end="")
        prev = p

def control_robot(file):
    r = Robot()
    s = State(parse_input(file))
    r.painted = {(0,0):1}
    while s.signal != "HALT":
        execute_all(s)
        if s.signal == "IN":
            s.inputs = [r.get_input()]
        elif s.signal == "OUT":
            r.paint(s.outputs.pop(0))
            execute_all(s)
            if s.signal != "OUT":
                raise Exception("Expected 2 OUTs in a row")
            r.turn_and_move(s.outputs.pop(0))
    print(len(r.painted))
    print_canvas(r.painted)


control_robot("./input")