def tokens():
    while True:
        for token in input().split():
            yield token

it = tokens()

def nextInt():
    return int(next(it))

def nextToken():
    return next(it)

def nextFloat():
    return float(next(it))

def bitAt(number, position):
    return (number >> position) & 1

def solve():
    x = nextInt()
    y = nextInt()

    # A xor 0 = A
    # A xor B <= A or <= B
    # max we can do 0 xor (x + y)
    s = x + y
    # but optimal amount of operations is less than x
    # x is the answer, but not optimal, let find better
    # we will move from highest one bit of s to low bits and build final x and y
    # biggest bit of s is always 1 and x and y can't be 1 and 1 at same time

    # guess, we will never face 1, 1, 1 - I can't prove it. But sound logical.
    # I only see why for HOB of s
    op = 0
    for bitInd in range(s.bit_length() - 1, 0, -1):
        if (bitAt(x, bitInd) + bitAt(y, bitInd)) % 2 != bitAt(s, bitInd) :
            # case 1 10 or 01 skip
            # case 1 00
            if bitAt(s,bitInd) == 1 and bitAt(x, bitInd) == bitAt(y, bitInd):
                assert bitAt(x, bitInd) == 0
                t = y
                y = ((y >> (bitInd+1)) << (bitInd+1)) + (1 << bitInd)
                x -= y - t
                op += y - t
            # elif
            # this file gave me the accepted from the first try. I don't like it.
            # was not able to prove why it's enough.
            pass


    print(s, op)

t = nextInt()
while t > 0:
    t -= 1
    solve()