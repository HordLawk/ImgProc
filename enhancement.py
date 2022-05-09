import numpy as np
import imageio
import math

filename = str(input()).rstrip()
I = imageio.imread(filename)
method = int(input())

def fn1():
    t = int(input())
    while(True):
        ti = t
        g1 = []
        g2 = []
        for i in range(len(I)):
            for k in range(len(I[i])):
                if(I[i][k] > ti):
                    g1.append(I[i][k])
                else:
                    g2.append(I[i][k])
        u1 = sum(g1) / len(g1)
        u2 = sum(g2) / len(g2)
        t = (u1 + u2) / 2
        if abs(t - ti) < 0.5:
            break
    Ip = np.zeros((len(I), len(I[0])), np.uint8)
    for i in range(len(I)):
        for k in range(len(I[i])):
            Ip[i][k] = np.uint8(I[i][k] > t)
    return Ip

def fn2():
    n = int(input())
    weightsStrings = input().split(' ', n)
    weights = np.array([float(weightsStrings[i]) for i in range(len(weightsStrings))])
    center = n >> 1
    Ia = I.flatten()
    Iaaux = np.pad(Ia, center, "wrap")
    Ipa = np.zeros(len(Ia))
    for i in range(center, len(Ipa) - center):
        Ipa[i - center] = sum(weights * Iaaux[i - center: i + center + 1])
    return np.reshape(Ipa, (len(I), len(I)))

def fn3():
    n = int(input())
    weights = []
    for i in range(n):
        weightsStrings = input().split(' ', n)
        weights.append([float(weightsStrings[i]) for i in range(len(weightsStrings))])
    t = int(input())
    Ipf = np.zeros((len(I), len(I[0])))
    center = len(weights) >> 1
    Iaux = np.pad(I, center, "edge")
    for i in range(center, len(Iaux) - center):
        for k in range(center, len(Iaux[i]) - center):
            Ipf[i - center][k - center] = sum((weights * Iaux[i - center:i + center + 1, k - center:k + center + 1]).flatten())
    while(True):
        ti = t
        g1 = []
        g2 = []
        for i in range(len(Ipf)):
            for k in range(len(Ipf[i])):
                if(Ipf[i][k] > ti):
                    g1.append(Ipf[i][k])
                else:
                    g2.append(Ipf[i][k])
        u1 = sum(g1) / len(g1)
        u2 = sum(g2) / len(g2)
        t = (u1 + u2) / 2
        if abs(t - ti) < 0.5:
            break
    Ip = np.zeros((len(Ipf), len(Ipf[0])), np.uint8)
    for i in range(len(Ipf)):
        for k in range(len(Ipf[i])):
            Ip[i][k] = np.uint8(Ipf[i][k] > t)
    return Ip

def fn4():
    n = int(input())
    center = n >> 1
    Iaux = np.pad(I, center, "constant", constant_values=0)
    Ip = np.zeros((len(I), len(I[0])), int)
    for i in range(center, len(Iaux) - center):
        for k in range(center, len(Iaux[i]) - center):
            neighbours = Iaux[i - center:i + center + 1, k - center:k + center + 1].flatten()
            neighbours.sort()
            Ip[i - center][k - center] = neighbours[(n * n) >> 1]
    return Ip

Ip = [fn1, fn2, fn3, fn4][method - 1]()
Ip = (((Ip - np.min(Ip)) / (np.max(Ip) - np.min(Ip)) * 255).astype(np.uint8))

sums = 0
for i in range(len(I)):
    for k in range(len(I[i])):
        sums += (I[i][k] - float(Ip[i][k])) ** 2
rse = math.sqrt(sums / (len(I) * len(I[0])))
print('{:.4f}'.format(rse))