def extended_euclidean(a, b):
    if b == 0:
        return (1, 0, a)
    else:
        x1, y1, d = extended_euclidean(b, a % b)
        x, y = y1, x1 - (a//b) * y1
        return(x, y, d)
p = 26513
q = 32321

u, v, g = extended_euclidean(p, q)
print(u, v, g)
print(min(u, v))