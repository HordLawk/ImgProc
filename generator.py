import numpy as np
import math
import random

filename = str(input()).rstrip()
R = np.load(filename)
sizec = int(input())
function = int(input())
q = int(input())
sizen = int(input())
bpp = int(input())
seed = int(input())

random.seed(seed)
c = np.zeros((sizec, sizec), float)

def fn1():
    for x in range(sizec):
        for y in range(sizec):
            c[x][y] = (x * y) + (2 * y)

def fn2():
    for x in range(sizec):
        for y in range(sizec):
            c[x][y] = abs(math.cos(x / q) + (2 * math.sin(y / q)))

def fn3():
    for x in range(sizec):
        for y in range(sizec):
            c[x][y] = abs((3 * (x / q)) - ((y / q) ** (1 / 3)))

def fn4():
    for x in range(sizec):
        for y in range(sizec):
            c[x][y] = random.random()

def fn5():
    x = y = 0
    c[x][y] = 1
    for i in range((sizec * sizec) + 1):
        x = ((x + random.randint(-1, 1)) % sizec)
        y = ((y + random.randint(-1, 1)) % sizec)
        c[x][y] = 1

# Assembles the functions in a list and uses the function number as the index
[fn1, fn2, fn3, fn4, fn5][function - 1]()

# Normalizes the scene to have values from 0 to 65535 (2^16 - 1)
c = (c - np.min(c)) / (np.max(c) - np.min(c))
c = (c * 65535)

# Maps the elements from the original image using the scene
n = np.zeros((sizen, sizen), float)
step = int(sizec / sizen)
for i in range(sizen):
    for k in range(sizen):
        n[i][k] = c[i * step][k *step]

# Normalizes the digital image to have values from 0 to 255, assigns the type to uint8 and shifts the bits to comply
# with the chosen bpp
n = (((n - np.min(n)) / (np.max(n) - np.min(n)) * 255).astype(np.uint8)) >> (8 - bpp)

# Calculates the RSE
sums = 0
for i in range(sizen):
    for k in range(sizen):
        sums += (float(n[i][k]) - R[i][k]) ** 2
rse = math.sqrt(sums)

print('{:.4f}'.format(rse))