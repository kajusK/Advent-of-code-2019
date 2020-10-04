#!/usr/bin/python3
from PIL import Image


def num2digits(num):
    res = []
    while num != 0:
        res.append(num % 10)
        num /= 10
        num = int(num)

    return res[::-1]


with open('input', 'r') as f:
    data = f.read().strip()

width = 25
height = 6
layer_size = width*height

layers = []
for i in range(0, len(data), layer_size):
    layer = list(data[i:i+layer_size])
    layers.append(list(map(lambda x: int(x), layer)))

min = 9999999999
min_i = -1

for i in range(len(layers)):
    zeros = layers[i].count(0)
    if zeros < min:
        min = zeros
        min_i = i

print(layers[min_i].count(1)*layers[min_i].count(2))

img = [0 for i in range(layer_size)]
for layer in layers[::-1]:
    for i in range(layer_size):
        if layer[i] != 2:
            img[i] = layer[i]

for i in range(0, layer_size, width):
    print(img[i:i+width])

