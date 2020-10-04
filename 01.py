#!/usr/bin/python3


def get_fuel(weight):
    return int(weight/3)-2


def fuel_req(fuel):
    add = fuel
    sum = fuel
    while True:
        add = get_fuel(add)
        if add <= 0:
            return sum
        sum += add


with open('input', 'r') as f:
    lines = f.readlines()

sum = 0
for line in lines:
    sum += fuel_req(get_fuel(int(line)))

print(sum)

