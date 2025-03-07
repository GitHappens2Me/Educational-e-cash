import math
import random

def modulo_inverse(x, m):
    def extended_gcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = extended_gcd(b % a, a)
            return (g, x - (b // a) * y, y)
    
    g, a, _ = extended_gcd(x, m)
    if g != 1:
        raise ValueError("Inverse doesn't exist")
    return a % m


def is_moduloinverse(d, e, mod):
    """Verify if d ≡ e⁻¹ mod (mod)"""
    return (e * d) % mod == 1

# to generate e so it is coprime to phi
def coprime(phi):
    """Finds suitable e value coprime with φ(n)"""
    # Try common RSA exponents first for efficiency
    for e in [65537, 17, 3, 5, 7, 13, 19]:
        if 1 < e < phi and math.gcd(e, phi) == 1:
            return e
    
    # Fallback to random search if needed
    while True:
        e = random.randint(2, phi - 1)
        if math.gcd(e, phi) == 1:
            return e
        
 
def is_coprime(a, b):
    return math.gcd(a, b) == 1