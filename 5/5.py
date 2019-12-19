import os
import sys

DEBUG = False

class State:
    instruction_counter: int = 0
    mem: list
    inputs: list = []
    outputs: list = []

    def __init__(self, mem: list, instruction_counter: int=0):
        self.mem = mem
        self.instruction_counter = instruction_counter

    def __str__(self):
        out = f"instruction_counter: {self.instruction_counter}\nmem:\n" 
        out += f"inputs: {self.inputs}, outputs: {self.outputs}\n"
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
        print(self)
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
        ins.savearg(state, 0, state.inputs.pop(0))
    elif ins.op == "OUT":
        state.outputs.append(ins.loadarg(state, 0))
    # jump instructions
    elif ins.op == "HALT":
        return True
    elif ins.op == "JPT":
        if ins.loadarg(state, 0) != 0:
            state.instruction_counter = ins.loadarg(state, 1)
            return False
    elif ins.op == "JPF":
        if ins.loadarg(state, 0) == 0:
            state.instruction_counter = ins.loadarg(state, 1)
            return False
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
    return False

def execute_all(state : State):
    if DEBUG:
        print("START")
        print(state)

    while True:
        should_exit = execute_next(state)
        if DEBUG:
            print(state)
        if should_exit:
            break

    if DEBUG:
        print("END")
        print(state)

def main(file):
    state = State(parse_input(file))
    state.inputs = [5]

    execute_all(state)
    print(state)

#main("sample3")
main("./input")