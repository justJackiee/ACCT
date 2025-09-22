from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

p = 991
g = 209

d = inverse(g, 991)
print(d)