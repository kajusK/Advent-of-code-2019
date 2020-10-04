#!/usr/bin/python3

moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def num2digits(num):
    res = []
    while num != 0:
        res.append(num % 10)
        num /= 10
        num = int(num)

    return res[::-1]


class IntcodePc:
    def __init__(self):
        with open('input', 'r') as f:
            self.code = f.read().strip().split(',')
            self.code = list(map(lambda x: int(x), self.code))
        self.reset()

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

    def reset(self):
        self.memory = self.code.copy() + [0]*10000
        self.pc = 0
        self.rel_base = 0
        self.input = []
        self.outreq = 0
        self.out = []

    def setInput(self, data):
        self.input = list(data)

    def setOutReq(self, count):
        self.outreq = count

    def run(self):
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
                if len(self.input) == 0:
                    raise ValueError("Unexpected input request")
                memory[self._writePos(modes, 1)] = self.input.pop(0)
                self.pc += 2
            # output
            elif op == 4:
                self.out.append(self._par(modes, 1))
                self.pc += 2
                if len(self.out) >= self.outreq:
                    out = self.out
                    self.out = []
                    if self.outreq == 1:
                        return out[0]
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
                raise ValueError("Incrorrect instruction")
        return True


def printMap(map):
    for y in range(len(map)):
        for x in range(len(map[0])):
            print(map[y][x], end='')
        print('')


def getIntersections(map):
    ints = []

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # ignore edges, no intersections there
    for y in range(1, len(map)-1):
        for x in range(1, len(map[0])-1):
            if map[y][x] != '#':
                continue

            found = True
            for dir in dirs:
                if map[y + dir[1]][x + dir[0]] != '#':
                    found = False
                    break
            if not found:
                continue
            ints.append((x, y))

    return ints


def calcPos(pos, dir):
    return (pos[0] + moves[dir][0], pos[1] + moves[dir][1])


def addBorder(map):
    new = [['O' for x in range(len(map[0]) + 2)]]
    for y in map:
        new.append(['O'] + y + ['O'])
    new.append(['O' for x in range(len(map[0]) + 2)])
    return new


# get list of commands needed to walk all positions in map
def walkMap(map, pos):
    # add border around map to avoid edge conditions
    map = addBorder(map)
    pos = (pos[0]+1, pos[1]+1)

    out = []

    c = map[pos[1]][pos[0]]
    if c == '^':
        dir = 0
    elif c == '>':
        dir = 1
    elif c == 'v':
        dir = 2
    elif c == '<':
        dir = 3
    else:
        exit("Unknown direction: "+c)

    straight = 0
    while True:
        x, y = calcPos(pos, dir)
        if map[y][x] == '#':
            pos = (x, y)
            straight += 1
            continue

        if straight != 0:
            out.append(str(straight))
            straight = 0
        x, y = calcPos(pos, (dir + 1) % 4)
        if map[y][x] == '#':
            dir = (dir + 1) % 4
            out.append('R')
            continue

        x, y = calcPos(pos, (dir - 1) % 4)
        if map[y][x] == '#':
            dir = (dir - 1) % 4
            out.append('L')
            continue

        break
    return out


# return true if group found at least twice in array (including itself)
def groupInArray(group, array):
    res = []

    for offset in range(len(array)-len(group)):
        found = True
        for x in range(len(group)):
            if group[x] != array[offset+x]:
                found = False
                break
        if found:
            res.append(offset)

    if len(res) < 2:
        return False
    return True


# replace all occurences in groups by A, B, C, return false if there
# are any commands not touched during replacement
def allReplaced(groups, steps):
    for i in range(len(groups)):
        steps = steps.replace(groups[i], chr(ord('A')+i))

    for c in steps:
        if c not in ['A', 'B', 'C', ',']:
            return False

    return steps


# brute-force all possible combinations of groups
def tryCombinations(steps, groups, maxLen):
    items = len(groups)
    for a in range(items):
        for b in range(a+1, items):
            for c in range(b+1, items):
                combo = [groups[a], groups[b], groups[c]]
                res = allReplaced(combo, steps)
                if res is not False and len(res) <= maxLen:
                    return (res, combo)


pc = IntcodePc()
pc.setOutReq(1)
map = []
line = []
start = None

out = pc.run()
while out is not True:
    c = chr(out)
    if c in ['^', '<', '>', 'v']:
        start = (len(line), len(map))

    if c != '\n':
        line.append(c)
    elif len(line) > 0:
        map.append(line)
        line = []
    out = pc.run()

ints = getIntersections(map)
printMap(map)

sum = 0
for pos in ints:
    sum += pos[0] * pos[1]

print("Sum of the alignment parameters:", sum)


maxLen = 20

steps = walkMap(map, start)
groups = []
# get all possible groups that are short enough according to rules
for l in range(int(maxLen/2), 2, -1):
    for offset in range(len(steps)-l+1):
        group = steps[offset:offset + l]
        if len(','.join(group)) > maxLen:
            continue
        # skip groups that doesn't start with dir and end with number
        if group[0] not in ['L', 'R'] or group[-1] in ['L', 'R']:
            continue
        if groupInArray(group, steps):
            groups.append(','.join(group))

# finally get one combination of groups that matches the rules
program = tryCombinations(','.join(steps), groups, maxLen)

data = program[0]+'\n'
for group in program[1]:
    data += group+'\n'
data += 'n\n'

print("command:\n--------\n"+data+"---------")

# convert data to ascii
data = list(data)
data = [ord(c) for c in data]

pc.reset()
pc.setOutReq(1)
pc.setInput(data)
pc.memory[0] = 2

# prints out the map, skip it and get the last data outputted
last = 0
while True:
    out = pc.run()
    if out is True:
        break
    last = out

print("dust collected:", last)
