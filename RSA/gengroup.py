import math
from factordb.factordb import FactorDB

def factorize(n):
    """Return the prime factorization of n as a list of prime factors."""
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
        if d * d > n:
            if n > 1:
                factors.append(n)
            break
    return factors

def get_prime_factors_set(n):
    """Return the set of unique prime factors of n."""
    return set(factorize(n))

def is_primitive_element(g, p):
    """
    Check if g is a primitive element modulo p.
    g is primitive if g^((p-1)/q) ≢ 1 (mod p) for all prime factors q of p-1
    """
    if g == 0:
        return False
        
    # Get p-1 and its prime factors
    phi = p - 1
    prime_factors = get_prime_factors_set(phi)
    
    # For each prime factor q of p-1, check if g^((p-1)/q) ≡ 1 (mod p)
    for q in prime_factors:
        if pow(g, phi // q, p) == 1:
            return False
    return True

def find_smallest_primitive_element(p):
    """Find the smallest primitive element modulo p."""
    g = 2
    while not is_primitive_element(g, p):
        g += 1
    return g

# Our prime p
p = 28151
# Find and print the smallest primitive element
result = find_smallest_primitive_element(p)
print(f"The smallest primitive element of F_{p} is: {result}")

f = FactorDB(p - 1)
f.connect()
print(f.get_factor_list())