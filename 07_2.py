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


class Amplifier:
    def __init__(self, memory, phase):
        self.memory = memory.copy()
        self.phase = phase
        self.pc = 0
        self.first_run = True

    def run(self, input):
        while self.memory[self.pc] != 99:
            op = self.memory[self.pc] % 100
            modes = num2digits(int(self.memory[self.pc]/100))[::-1]

            # sum
            if op == 1:
                par1 = par(self.memory, self.pc, modes, 1)
                par2 = par(self.memory, self.pc, modes, 2)
                self.memory[self.memory[self.pc+3]] = par1+par2
                self.pc += 4
            # multiply
            elif op == 2:
                par1 = par(self.memory, self.pc, modes, 1)
                par2 = par(self.memory, self.pc, modes, 2)
                self.memory[self.memory[self.pc+3]] = par1*par2
                self.pc += 4
            # input
            elif op == 3:
                if self.first_run:
                    data = self.phase
                    self.first_run = False
                else:
                    data = input
                self.memory[self.memory[self.pc+1]] = data
                self.pc += 2
            # output
            elif op == 4:
                data = par(self.memory, self.pc, modes, 1)
                self.pc += 2
                return data
            # jump if true
            elif op == 5:
                if par(self.memory, self.pc, modes, 1):
                    self.pc = par(self.memory, self.pc, modes, 2)
                else:
                    self.pc += 3
            # jump if false
            elif op == 6:
                if not par(self.memory, self.pc, modes, 1):
                    self.pc = par(self.memory, self.pc, modes, 2)
                else:
                    self.pc += 3
            # less than
            elif op == 7:
                par1 = par(self.memory, self.pc, modes, 1)
                par2 = par(self.memory, self.pc, modes, 2)
                self.memory[self.memory[self.pc+3]] = 1 if par1 < par2 else 0
                self.pc += 4
            # equals
            elif op == 8:
                par1 = par(self.memory, self.pc, modes, 1)
                par2 = par(self.memory, self.pc, modes, 2)
                self.memory[self.memory[self.pc+3]] = 1 if par1 == par2 else 0
                self.pc += 4
            else:
                exit("Incorrect!!!")
        return True


def get_gain(memory, phases):
    amps = []
    for phase in phases:
        amps.append(Amplifier(memory, phase))

    last = 0
    data = 0
    while True:
        for i in range(len(phases)):
            data = amps[i].run(data)
            if type(data) == bool:
                return last
        last = data


def try_phases(memory):
    phase = 56788
    max = 0

    while phase < 100000:
        phase += 1
        data = num2digits(phase)
        if len(set([5, 6, 7, 8, 9]) & set(data)) != 5:
            continue

        out = get_gain(memory, data)
        if out > max:
            max = out
    return max


with open('input', 'r') as f:
    memory = f.read().strip().split(',')
    memory = list(map(lambda x: int(x), memory))

print(try_phases(memory))
