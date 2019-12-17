import os
import sys

DEBUG = False

class State:
    program_counter: int = 0
    mem: list
    def __init__(self, mem: list, program_counter: int=0):
        self.mem = mem
        self.program_counter = program_counter

    def __str__(self):
        out = f"program_counter: {self.program_counter}\nmem:\n" 
        i = 0
        for n in range(0,10):
            out += f"\t{n}"
        out += f"\n-----------------------------------------------------------------------------------\n"
        while (i < len(self.mem)):
            if (i == self.program_counter):
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
  
OPCODES = {
    1:"ADD", 
    2:"MUL",
    99:"HALT"}
# Returns {op: "ADD", src: 0, trg: 1, dst: 21}
def decode_ins(ins):
    if len(ins) < 4:
        opcode = OPCODES[ins[0]]
        if opcode != "HALT":
            raise Exception(f"Shortened instruction that is not HALT {ins}")
        return {"op": opcode}

    return {"op": OPCODES[ins[0]], "src": ins[1], "trg": ins[2], "dst": ins[3]}

# Execute next instruction, return true if HALT
def execute_next(state : State):  
    ins = decode_ins(state.mem[state.program_counter : state.program_counter + 4])
    if DEBUG:
        print(ins)
    if ins["op"] == "ADD":
        state.mem[ins["dst"]] = state.mem[ins["src"]] + state.mem[ins["trg"]]
    elif ins["op"] == "MUL":
        state.mem[ins["dst"]] = state.mem[ins["src"]] * state.mem[ins["trg"]]
    elif ins["op"] == "HALT":
        return True

    state.program_counter += 4
    return False

def main(file):
    state = State(parse_input(file))
    # kill me, just for 2a
    state.mem[1] = 12
    state.mem[2] = 2

    print("START")
    print(state)

    while True:
        should_exit = execute_next(state)
        if DEBUG:
            print(state)
        if should_exit:
            break
    print("END")
    print(state)

#main("sample3.txt")
main("./input.txt")