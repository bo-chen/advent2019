import os
import sys

DEBUG = False

class State:
    instruction_counter: int
    mem: list
    inputs: list
    outputs: list
    signal: str

    def __init__(self, mem: list, instruction_counter: int=0):
        self.instruction_counter = 0
        self.mem = mem
        self.instruction_counter = instruction_counter
        self.inputs = []
        self.outputs = []
        self.signal = None

    def __str__(self):
        i = 0
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
        out = f"instruction_counter: {self.instruction_counter}\nmem:\n" 
        out += f"inputs: {self.inputs}, outputs: {self.outputs}\n"
        out += f"signal: {self.signal}\n"
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
        if self.argmodes[pos] != "0":
            raise Exception("Wrong argmode to save", self)
        state.mem[self.args[pos]] =  val

    def loadarg(self, state : State, pos : int):
        mode = self.argmodes[pos]
        if mode == "0":
            return state.mem[self.args[pos]]
        elif mode == "1":
            return self.args[pos]
        else:
            raise Exception("Unknown argmode", str(self))

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
        print(state)
    
    return signal

def genperms(settings):
    if not settings:
        return [[]]
    perms = []
    for n in settings:
        ns = list(settings)
        ns.remove(n)
        os = map(lambda x: [n] + x, genperms(ns))
        perms.extend(os)
    return perms

def execute_feedback(file, setting):
    amps = []
    for n in range(5):
        s = State(parse_input(file))
        s.inputs = [setting[n]]
        amps.append(s)

    n = 0
    power = 0
    while True:
        s = amps[n]
        if s.signal == "HALT":
            # print(f"next amp {n} is halted, returning")
            return power
        s.inputs.append(power)
        execute_all(s)
        # There should only be an output signal now
        if s.signal == "IN" or s.signal == "HALT":
            raise Exception("Unexpected input request")
        power = s.outputs.pop(0)
        # Run again to get to the next IN or HALT
        execute_all(s)
        # if s.signal == "HALT":
            # print(f"amp {n} halted")
        n = (n + 1) % 5

ps = genperms([9,8,7,6,5])
print(len(ps))
m = 0
for ss in ps:
    p = execute_feedback("./input",ss)
    if p > m:
        m = p

print(m)