#!/usr/bin/python3
import copy

moves = [(-1, 0),
         (1, 0),
         (0, -1),
         (0, 1)]


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
                out = self._par(modes, 1)
                self.pc += 2
                return out
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


def mapPrint(map):
    for y in range(len(map)):
        for x in range(len(map[0])):
            print(str(map[y][x]), end='')
        print('')


def calcPos(pos, dir):
    return (pos[0] + moves[dir][0], pos[1] + moves[dir][1])


def getFromDir(dir):
    if dir == 0:
        return 1
    if dir == 1:
        return 0
    if dir == 2:
        return 3
    if dir == 3:
        return 2


def nextDir(room):
    for dir in range(0, 4):
        if room[dir] == 0:
            return dir

    for dir in range(0, 4):
        if room[dir] == 'I':
            return dir

    return None


def roomNotVisited(room):
    for dir in range(0, 4):
        if room[dir] != 0:
            return False
    return True


# Using tarrys alogithm - mark entry direction to each cell (if cell is not
# visited yet], mark out direction when leaving cell. Next direction is one
# that is not marked yet or if all directions are marked, use in direction,
# if all directions are out, whole maze was explored
def getMap(size_x, size_y, start_x, start_y):
    with open('input', 'r') as f:
        memory = f.read().strip().split(',')
        memory = list(map(lambda x: int(x), memory))

    pc = IntcodePc(memory)

    pos = (start_x, start_y)
    oxygen = None
    dir = 0

    doors = [[[0, 0, 0, 0] for x in range(size_x)] for y in range(size_y)]

    maze = [['.' for x in range(size_x)] for y in range(size_y)]
    maze[pos[1]][pos[0]] = ' '

    while dir is not None:
        out = pc.run(dir+1)
        # wall
        if out == 0:
            doors[pos[1]][pos[0]][dir] = 'W'
            (x, y) = calcPos(pos, dir)
            maze[y][x] = '#'
        # empty space
        elif out == 1 or out == 2:
            doors[pos[1]][pos[0]][dir] = 'O'
            pos = calcPos(pos, dir)
            maze[pos[1]][pos[0]] = ' '
            if roomNotVisited(doors[pos[1]][pos[0]]):
                doors[pos[1]][pos[0]][getFromDir(dir)] = 'I'
            if out == 2:
                oxygen = pos
        else:
            exit("Wtf")

        dir = nextDir(doors[pos[1]][pos[0]])

    return (maze, oxygen)


# for earch visited cell, mark all neighbours with index number plus one if
# not marked yet and append these to queue from which points are taken for
# processing
def getDistance(map, start_pos, end_pos):
    map[start_pos[1]][start_pos[0]] = 0
    queue = [start_pos]

    while len(queue) > 0:
        pos = queue.pop(0)
        count = map[pos[1]][pos[0]]

        if pos == end_pos:
            return count

        for dir in range(0, 4):
            x, y = calcPos(pos, dir)
            if map[y][x] != ' ':
                continue
            map[y][x] = count + 1
            queue.append((x, y))


def getFilling(map, start):
    queue = [start]
    map[start[1]][start[0]] = 0
    max_count = 0

    while len(queue) > 0:
        pos = queue.pop(0)
        count = map[pos[1]][pos[0]]
        if count > max_count:
            max_count = count

        for dir in range(0, 4):
            x, y = calcPos(pos, dir)
            if map[y][x] != ' ':
                continue
            map[y][x] = count + 1
            queue.append((x, y))

    return max_count


size_x = 45
size_y = 45
start_x = int(size_x/2)
start_y = int(size_y/2)

mazeMap, oxygen = getMap(45, 45, start_x, start_y)
mapPrint(mazeMap)
print("==============")
dist = getDistance(copy.deepcopy(mazeMap), (start_x, start_y), oxygen)
print("distance to oxygen:", dist)
filling_t = getFilling(copy.deepcopy(mazeMap), oxygen)
print("filling time:", filling_t)
