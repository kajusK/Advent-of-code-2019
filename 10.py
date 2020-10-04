#!/usr/bin/python3

from fractions import Fraction
from pprint import pprint


def sign(x):
    if (x >= 0):
        return 1
    return -1


# all points with the same dist_x/dist_y ration in the given direction
# can shade the asteroid on x2, y2
def is_visible(x1, y1, x2, y2, space):
    if x1 == x2 and y1 == y2:
        return False

    # will make fraction and
    if x1 - x2 == 0:
        step_y = sign(y2-y1)
        step_x = 0
    elif y1 - y2 == 0:
        step_y = 0
        step_x = sign(x2-x1)
    else:
        frac = Fraction(abs(x1 - x2), abs(y2 - y1))
        step_x = sign(x2-x1)*frac.numerator
        step_y = sign(y2-y1)*frac.denominator
    x = x1 + step_x
    y = y1 + step_y

    while x != x2 or y != y2:
        if space[y][x] == '#':
            return False
        x += step_x
        y += step_y
    return True


def count_visible(x, y, space):
    # we can see ourself
    visible = 0
    for y1 in range(len(space)):
        for x1 in range(len(space[0])):
            if space[y1][x1] != '#':
                continue
            if is_visible(x, y, x1, y1, space):
                visible += 1
    return visible


# return "angle" (quadrant, abs(y/x))
def get_angle(x1, y1, x2, y2):
    if x2 >= x1:
        if y2 < y1:
            quadrant = 0
        elif x2 != x1:
            quadrant = 1
        else:
            quadrant = 2
    else:
        if y2 <= y1:
            quadrant = 3
        else:
            quadrant = 2

    if y2 == y1 or x2 == x1:
        return quadrant*1000

    if quadrant == 0 or quadrant == 2:
        angle = abs((x2-x1)/(y2-y1))
    else:
        angle = abs((y2-y1)/(x2-x1))
    return quadrant*1000 + angle


def vaporize(x, y, space, search_for):
    # mark every point with angle
    angles = {}
    for y1 in range(len(space)):
        for x1 in range(len(space[0])):
            if space[y1][x1] != '#':
                continue
            angle = round(get_angle(x, y, x1, y1), 3)
            if angle not in angles:
                angles[angle] = []
            angles[angle].append((x1, y1))

    rem_count = 0
    while True:
        for key in sorted(angles):
            for i, pos in enumerate(angles[key]):
                # would be easier to remove first asteroid hit, but more coding
                # it's late night and I'm lazy
                if space[pos[1]][pos[0]] != '#':
                    continue
                if not is_visible(x, y, pos[0], pos[1], space):
                    continue
                rem_count += 1
                if rem_count == search_for:
                    print("removed 200th at", pos)
                    return
                space[pos[1]][pos[0]] = rem_count
                # TODO remove already used elements from array
                break
    pprint(angles)
    pprint(space)


space = []
with open('input', 'r') as f:
    for line in f:
        space.append(list(line.strip()))

size_y = len(space)
size_x = len(space[0])

max_visible = 0
coord = None
for y in range(size_y):
    for x in range(size_x):
        if space[y][x] != '#':
            continue
        visible = count_visible(x, y, space)
        if visible > max_visible:
            coord = (x, y)
            max_visible = visible

print(max_visible, "at", coord)
vaporize(coord[0], coord[1], space, 200)
