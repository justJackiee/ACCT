import math
from Crypto.Util.number import long_to_bytes

print(pow(101, 17, 22663))


p = 17
q = 23
N = p * q
e = 65537

print(pow(12, e, N))


# Euler's totient (ϕ(N) = (p-1)(q-1))
ϕ = (857504083339712752489993810777 - 1) * (1029224947942998075080348647219 - 1)
print(ϕ)

d = pow(e, -1, ϕ)
print(d)

N = 882564595536224140639625987659416029426239230804614613279163

c = 77578995801157823671636298847186723593814843845525223303932
# Decrypt M = c^d (mod N)
print(pow(c, d, N))