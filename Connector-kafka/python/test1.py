from math import ceil

n, q = [int(i) for i in input().split(' ')]
res = 0
b = 0
for i in range(n):
    cost, gain = [int(i) for i in input().split(' ')]
    if gain * q > cost:
        res += gain
        b += cost
print(res - ceil(b/q))
