#!/usr/bin/python3


def is_valid(digits):
    prev = digits[0]-1
    grp_len = 0
    doubles = 0

    for d in digits:
        if prev == d:
            grp_len += 1
            doubles += 1
        else:
            if grp_len and grp_len > 1:
                doubles -= grp_len
            grp_len = 0

        if prev > d:
            return False
        prev = d

    if grp_len and grp_len > 1:
        doubles -= grp_len
    if doubles:
        return True
    return False


def num2digits(num):
    res = []
    while num != 0:
        res.append(num % 10)
        num /= 10
        num = int(num)

    return res[::-1]


rmin = 128392
rmax = 643281

cnt = 0
for num in range(rmin, rmax + 1):
    digits = num2digits(num)
    if is_valid(digits):
        cnt += 1

print(cnt)
