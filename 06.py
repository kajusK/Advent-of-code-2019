#!/usr/bin/python3

from pprint import pprint


def count_orbits(node, depth=0):
    # relation to parent
    orbits = 1
    for child in node['children']:
        orbits += count_orbits(child, depth+1)

    return orbits + depth


def get_parents(node, name, parents):
    if name == node['name']:
        return True
    for child in node['children']:
        found = get_parents(child, name, parents)
        if found:
            parents.append(node['name'])
            return found
    return False


def build_tree(orbits, name='COM'):
    node = {'name': name, 'children': []}
    if name not in orbits:
        return node
    for child in orbits[name]:
        node['children'].append(build_tree(orbits, child))

    return node


orbits = {}
with open('input', 'r') as f:
    for line in f:
        spl = line.strip().split(')')
        parent = spl[0]
        name = spl[1]
        if parent not in orbits:
            orbits[parent] = []
        orbits[parent].append(name)

tree = build_tree(orbits)
parents1 = []
parents2 = []
found1 = get_parents(tree, 'YOU', parents1)
found2 = get_parents(tree, 'SAN', parents2)

route = set(parents1) ^ set(parents2)
pprint(route)
print(len(route))
