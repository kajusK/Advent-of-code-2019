#!/usr/bin/python3
from pprint import pprint


class IntcodePc:
    def __init__(self, program):
        self.memory = program.copy()+[0]*10000
        self.pc = 0
        self.rel_base = 0

    def _getMode(self, modes, pos):
        if len(modes) >= pos:
            return modes[pos - 1]
        else:
            return 0

    def _getAddr(self, mode, pos):
        # position mode
        if mode == 0:
            addr = self.memory[self.pc + pos]
        # absolute mode
        elif mode == 1:
            addr = self.pc + pos
        # relative mode
        elif mode == 2:
            addr = self.memory[self.pc + pos] + self.rel_base
        else:
            raise ValueError("Unknown mode %d!!!" % (mode))
        return addr

    def _par(self, modes, pos):
        mode = self._getMode(modes, pos)
        return self.memory[self._getAddr(mode, pos)]

    def _writePos(self, modes, pos):
        mode = self._getMode(modes, pos)
        if mode == 1:
            raise ValueError("Absolute addresing in write request destination")
        return self._getAddr(mode, pos)

    def run(self, input):
        outs = []
        memory = self.memory

        while memory[self.pc] != 99:
            op = memory[self.pc] % 100
            modes = num2digits(int(memory[self.pc]/100))[::-1]

            # sum
            if op == 1:
                par1 = self._par(modes, 1)
                par2 = self._par(modes, 2)
                memory[self._writePos(modes, 3)] = par1+par2
                self.pc += 4
            # multiply
            elif op == 2:
                par1 = self._par(modes, 1)
                par2 = self._par(modes, 2)
                memory[self._writePos(modes, 3)] = par1*par2
                self.pc += 4
            # input
            elif op == 3:
                memory[self._writePos(modes, 1)] = input
                self.pc += 2
            # output
            elif op == 4:
                outs.append(self._par(modes, 1))
                self.pc += 2
                if len(outs) == 2:
                    return outs
            # jump if true
            elif op == 5:
                if self._par(modes, 1):
                    self.pc = self._par(modes, 2)
                else:
                    self.pc += 3
            # jump if false
            elif op == 6:
                if not self._par(modes, 1):
                    self.pc = self._par(modes, 2)
                else:
                    self.pc += 3
            # less than
            elif op == 7:
                par1 = self._par(modes, 1)
                par2 = self._par(modes, 2)
                memory[self._writePos(modes, 3)] = 1 if par1 < par2 else 0
                self.pc += 4
            # equals
            elif op == 8:
                par1 = self._par(modes, 1)
                par2 = self._par(modes, 2)
                memory[self._writePos(modes, 3)] = 1 if par1 == par2 else 0
                self.pc += 4
            # relative base settings
            elif op == 9:
                par1 = self._par(modes, 1)
                self.rel_base += par1
                self.pc += 2
            else:
                exit("Incorrect!!!")
        return True


def num2digits(num):
    res = []
    while num != 0:
        res.append(num % 10)
        num /= 10
        num = int(num)

    return res[::-1]


with open('input', 'r') as f:
    memory = f.read().strip().split(',')
    memory = list(map(lambda x: int(x), memory))

pc = IntcodePc(memory)

dirs = [
    (0, -1),
    (-1, 0),
    (0, 1),
    (1, 0)]
dir = 0
pos = (0, 0)
painted = {(0, 0): 1}

while True:
    color = 0
    if pos in painted:
        color = painted[pos]

    outs = pc.run(color)
    if outs is True:
        break
    painted[pos] = outs[0]

    if outs[1] == 0:
        dir += 1
    else:
        dir -= 1
    dir = dir % len(dirs)
    # move one step
    pos = (pos[0] + dirs[dir][0], pos[1] + dirs[dir][1])

map = [[0 for i in range(50)] for i in range(10)]
for pos, col in painted.items():
    char = ' '
    if col == 1:
        char = '#'

    map[pos[1]][pos[0]] = char

for y in range(len(map)):
    for x in range(len(map[0])):
        print(map[y][x], end='')
    print('')
