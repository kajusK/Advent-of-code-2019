#!/usr/bin/python3


class IntcodePc:
    def __init__(self, program):
        self.memory = program.copy()+[0]*10000
        self.pc = 0
        self.rel_base = 0
        self.input = None

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

    def run(self):
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
                if self.input is None:
                    return False
                memory[self._writePos(modes, 1)] = self.input
                self.input = None
                self.pc += 2
            # output
            elif op == 4:
                outs.append(self._par(modes, 1))
                self.pc += 2
                if len(outs) == 3:
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


def printMap(map, score):
    print("Score: ", score)
    for y in range(len(map)):
        for x in range(len(map[0])):
            item = map[y][x]
            c = ''
            if item == 0:
                c = ' '
            elif item == 1:
                c = '#'
            elif item == 2:
                c = 'b'
            elif item == 3:
                c = '-'
            elif item == 4:
                c = 'O'
            print(c, end='')
        print('')


def getMove(ball, paddle):
    if ball is None or paddle is None:
        return 0

    if paddle > ball:
        return -1
    if paddle < ball:
        return 1
    return 0


with open('input', 'r') as f:
    memory = f.read().strip().split(',')
    memory = list(map(lambda x: int(x), memory))

memory[0] = 2
pc = IntcodePc(memory)

size_x = 40
size_y = 20
map = [[0 for i in range(size_x)] for i in range(size_y)]

move = 0
score = 0
ball_pos = None
paddle_pos = None

while True:
    outs = pc.run()
    if outs is True:
        break
    if outs is False:
        move = getMove(ball_pos, paddle_pos)
        print(move, ball_pos, paddle_pos)
        printMap(map, score)
        pc.input = move
        continue
    if outs[0] == -1 and outs[1] == 0:
        score = outs[2]
        continue

    map[outs[1]][outs[0]] = outs[2]
    if outs[2] == 4:
        ball_pos = outs[0]
    if outs[2] == 3:
        paddle_pos = outs[0]

print(score)
