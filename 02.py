#!/usr/bin/python3


def run(memory, noun, verb):
    pc = 0

    memory[1] = noun
    memory[2] = verb

    while memory[pc] != 99:
        op = memory[pc]
        p1 = memory[pc+1]
        p2 = memory[pc+2]
        p3 = memory[pc+3]

        if op == 1:
            memory[p3] = memory[p1]+memory[p2]
            pc += 4
        elif op == 2:
            memory[p3] = memory[p1]*memory[p2]
            pc += 4
        else:
            exit("Incorrect!!!")
    return memory[0]


with open('input', 'r') as f:
    memory = f.read().strip().split(',')
    memory = list(map(lambda x: int(x), memory))

for noun in range(0, 100):
    for verb in range(0, 100):
        if run(memory.copy(), noun, verb) == 19690720:
            print(100*noun + verb)
            exit(0)
