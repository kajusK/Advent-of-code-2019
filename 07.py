#!/usr/bin/python3


def num2digits(num):
    res = []
    while num != 0:
        res.append(num % 10)
        num /= 10
        num = int(num)

    return res[::-1]


def par(memory, pc, modes, pos):
    if len(modes) >= pos:
        mode = modes[pos - 1]
    else:
        mode = 0

    # position mode
    if mode == 0:
        addr = memory[pc + pos]
        return memory[addr]

    return memory[pc + pos]


def run(memory, phase, input):
    in_count = 0
    memory = memory.copy()
    pc = 0

    while memory[pc] != 99:
        op = memory[pc] % 100
        modes = num2digits(int(memory[pc]/100))[::-1]

        # sum
        if op == 1:
            par1 = par(memory, pc, modes, 1)
            par2 = par(memory, pc, modes, 2)
            memory[memory[pc+3]] = par1+par2
            pc += 4
        # multiply
        elif op == 2:
            par1 = par(memory, pc, modes, 1)
            par2 = par(memory, pc, modes, 2)
            memory[memory[pc+3]] = par1*par2
            pc += 4
        # input
        elif op == 3:
            if in_count == 0:
                data = phase
                in_count += 1
            else:
                data = input

            memory[memory[pc+1]] = data
            pc += 2
        # output
        elif op == 4:
            return par(memory, pc, modes, 1)
            pc += 2
        # jump if true
        elif op == 5:
            if par(memory, pc, modes, 1):
                pc = par(memory, pc, modes, 2)
            else:
                pc += 3
        # jump if false
        elif op == 6:
            if not par(memory, pc, modes, 1):
                pc = par(memory, pc, modes, 2)
            else:
                pc += 3
        # less than
        elif op == 7:
            par1 = par(memory, pc, modes, 1)
            par2 = par(memory, pc, modes, 2)
            memory[memory[pc+3]] = 1 if par1 < par2 else 0
            pc += 4
        # equals
        elif op == 8:
            par1 = par(memory, pc, modes, 1)
            par2 = par(memory, pc, modes, 2)
            memory[memory[pc+3]] = 1 if par1 == par2 else 0
            pc += 4
        else:
            exit("Incorrect!!!")


def try_phases(memory, input, remaining, used=[]):
    if remaining == 0:
        return input
    max = 0
    for phase in range(0, 5):
        if phase in used:
            continue
        output = run(memory, phase, input)
        skip = used.copy()
        skip.append(phase)
        res = try_phases(memory, output, remaining-1, skip)
        if res > max:
            max = res

    return max


with open('input', 'r') as f:
    memory = f.read().strip().split(',')
    memory = list(map(lambda x: int(x), memory))


print(try_phases(memory, 0, 5))
