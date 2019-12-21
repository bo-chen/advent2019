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
            state.mem.extend([0] * (addr - len(state.mem) + 1))
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


def print_tile(v):
    c = "  "
    if v == 0:
        c = "  "
    elif v == 1:
        c = "XX"
    elif v == 2:
        c = "%%"
    elif v == 3:
        c = "/\\"
    elif v == 4:
        c = "()"
    else:
        raise Exception("Unknown tile value")
    print(c, end="")

def print_screen(ps):
    ordered = list(sorted(ps.items(), key=lambda p: p[0][1] * 10000000 + p[0][0]))
    prev = ordered.pop(0)
    print("  " * prev[0][0], end="")
    print_tile(prev[1])
    for p in ordered:
        if p[0][1] > prev[0][1]:
            print("\n" * (p[0][1] - prev[0][1]), end="")
            print("  " * p[0][0], end="")
            print_tile(p[1])
        elif p[0][1] > prev[0][1]:
            raise Exception("wrong sort order")
        else:
            print("  " * (p[0][0] - prev[0][0] - 1), end="")
            print_tile(p[1])
        prev = p
    print("")

def game(file):
    s = State(parse_input(file))
    # start game
    s.mem[0] = 2
    canvas = {}
    score = 0
    ball_x = 0
    paddle_x = 0
    while True:
        execute_all(s)
        if s.signal == "HALT":
            break
        elif s.signal == "OUT":
            execute_all(s)
            execute_all(s)
            if s.outputs[0] >= 0 and s.outputs[2] == 3:
                paddle_x = s.outputs[0]
            if s.outputs[0] >= 0 and s.outputs[2] == 4:
                ball_x = s.outputs[0]
            if s.outputs[0]  == -1 and s.outputs[1] == 0:
                score = s.outputs[2]
            elif s.outputs[0] < 0 or s.outputs[1] < 0:
                raise Exception("Unexpected negative output")
            else:
                canvas[(s.outputs[0], s.outputs[1])] = s.outputs[2]
            s.outputs = []
        elif s.signal == "IN":
            # print(s)
            print_screen(canvas)
            print(f"Current score: {score}")
            print(ball_x, paddle_x)
            # j = input("<Move Now>")
            s.inputs.append(ball_x - paddle_x)
            # Bit of cheating doesn't hurt
            s.mem[392] = s.mem[388]
        else:
            raise Exception("Unexpected signal")
    
    print_screen(canvas)
    print(f"Current score: {score}")

game("./input")