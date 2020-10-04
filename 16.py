#!/usr/bin/python3
import math


def num2digits(num):
    res = []
    while num != 0:
        res.append(num % 10)
        num /= 10
        num = int(num)

    return res[::-1]


def getPattern(pos):
    base = [0, 1, 0, -1]
    pos += 1
    pattern = []

    for i in range(pos*4):
        pattern.append(base[math.floor(i/pos)])
    return pattern


def fft(data):
    out = []

    for pos in range(len(data)):
        pattern = getPattern(pos)

        res = 0
        for i in range(len(data)):
            res += data[i] * pattern[(i+1) % len(pattern)]

        if res < 0:
            res = -res
        out.append(res % 10)
    return out


# if skip is over half of the data length, result for is obtained by summing
# numbers from offset to end,...
# out[n] = sum(data[n+1] + .. + data[len(data)-1]) % 10
def fftmod(data):
    new = [0 for i in range(len(data))]
    sum = 0
    for pos in range(len(data) - 1, -1, -1):
        sum += data[pos]
        new[pos] = sum % 10
    return new


def part1(data):
    phases = 100
    for i in range(phases):
        data = fft(data)
    print(''.join(map(lambda x: str(x), data[0:8])))


def part2(data, offset, repeat=10000):
    length = len(data)*repeat
    if offset < length/2:
        print("Works only for offsets over half of the input len")
        return False

    new = []
    for i in range(repeat):
        new += data
    data = new[offset:]

    phases = 100
    for i in range(phases):
        data = fftmod(data)

    print(''.join(map(lambda x: str(x), data[0:8])))


with open("input", "r") as f:
    data = list(f.read().strip())

offset = int(''.join(data[0:7]))
data = list(map(lambda x: int(x), data))

print("part1:", end="")
part1(data.copy())
print("part2:", end="")
part2(data.copy(), offset)
