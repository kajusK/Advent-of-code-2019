#!/usr/bin/python3

width = 30000
height = 30000
start_x = int(width/2)
start_y = int(height/2)


def walk(line, intersection=False):
    cmds = line.split(',')
    x = start_x
    y = start_y
    points = []
    steps = 0
    dists = {}

    for cmd in cmds:
        dist = int(cmd[1:])
        if cmd[0] == 'U':
            dir = [0, 1]
        elif cmd[0] == 'D':
            dir = [0, -1]
        elif cmd[0] == 'L':
            dir = [-1, 0]
        elif cmd[0] == 'R':
            dir = [1, 0]
        else:
            exit("Unknown dir:"+cmd[0])

        for i in range(dist):
            x += dir[0]
            y += dir[1]
            steps += 1
            points.append((x, y))
            if intersection and (x, y) in intersection:
                dists[(x, y)] = steps

    if intersection:
        return dists
    else:
        return set(points)


with open('input', 'r') as f:
    lines = f.readlines()

line1 = walk(lines[0])
line2 = walk(lines[1])

crosses = line1.intersection(line2)
min_dist = None

for cross in crosses:
    dist = abs(start_x - cross[0]) + abs(start_y - cross[1])
    if min_dist is None or dist < min_dist:
        min_dist = dist

print("Min dist normal: ", min_dist)

dist1 = walk(lines[0], crosses)
dist2 = walk(lines[1], crosses)
min_sum = None
for pos, dist in dist1.items():
    sum = dist + dist2[pos]
    if min_sum is None or sum < min_sum:
        min_sum = sum

print("Min length: ", min_sum)
