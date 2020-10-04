#!/usr/bin/python3

import re
from pprint import pprint


class Object:
    def __init__(self, x, y, z):
        self.pos = [x, y, z]
        self.velocity = [0, 0, 0]

    def getCoord(self):
        return self.pos

    def updateVelocity(self, coord):
        for i in range(3):
            if self.pos[i] == coord[i]:
                continue
            elif self.pos[i] < coord[i]:
                self.velocity[i] += 1
            elif self.pos[i] > coord[i]:
                self.velocity[i] -= 1

    def updatePosition(self):
        for i in range(3):
            self.pos[i] += self.velocity[i]

    def getEnergy(self):
        potential = abs(self.pos[0]) + abs(self.pos[1]) + abs(self.pos[2])
        kinetic = abs(self.velocity[0]) + abs(self.velocity[1]) + abs(self.velocity[2])
        return potential * kinetic

    def getState(self, i):
        return (self.pos[i], self.velocity[i])


def checkSame(target, init, coord):
    for i in range(len(init)):
        if target[i][coord] != init[i][coord]:
            return False

    return True


def getState(objects):
    state = []
    for a in range(len(objects)):
        substate = []
        for i in range(3):
            substate.append(objects[a].getState(i))
        state.append(substate)
    return state


# least common multiple
def lcm(x, y):
    return (x*y)/gcd(x, y)


# greatest common divisor
def gcd(x, y):
    remainder = 0
    while y != 0:
        remainder = x % y
        x = y
        y = remainder
    return x


objects = []
with open('input', 'r') as f:
    for line in f:
        match = re.findall(r'([xyz])=([-]?[0-9]+)', line)
        x = 0
        y = 0
        z = 0
        for coord in match:
            if coord[0] == 'x':
                x = int(coord[1])
            elif coord[0] == 'y':
                y = int(coord[1])
            elif coord[0] == 'z':
                z = int(coord[1])
        objects.append(Object(x, y, z))

found = [0, 0, 0]
found_count = 0
count = 0
init_state = getState(objects)

while found_count != 3:
    state = getState(objects)
    for a in range(len(objects)):
        for b in range(len(objects)):
            if a == b:
                continue
            objects[a].updateVelocity(objects[b].getCoord())

    for i in range(3):
        if found[i] or count == 0:
            continue
        if checkSame(state, init_state, i):
            found[i] = count
            found_count += 1
    count += 1
    for a in range(len(objects)):
        objects[a].updatePosition()

pprint(found)

a = lcm(found[0], found[1])
print(lcm(a, found[2]))
