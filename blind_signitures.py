from helper import modulo_inverse, is_coprime
from random import randint

## Toy Example of Blind Signatures as described in "Blind Signatures for untracable Payments" by David Chaum

## Three Functions are necessary: 

## Signing Function s'
## Only known to the Signer (Mint)
def private_sign(msg: int) -> int:
    """s' - Signer's private operation (RSA decryption)"""
    return pow(msg, d, n)

## and its inverse s
## publicly known
## such that: s(s'(x)) = x and s gives no info about s'
def public_verify(sig: int) -> int:
    """s - Public verification (RSA encryption)"""
    return pow(sig, e, n)

## Commuting (Blinding-) Function c
## Only known to the Provider (User)
def blind_message(msg: int, r: int) -> int:
    """c - Blinding operation (commuting function)"""
    return (msg * (pow(r, e, n))) % n

## And its inverse c'
## Only known to the Provider (User)
## such that: c'(s'(c(x))) = s'(x) and c(x) and s' give no info about x
def unblind_signature(blinded_sig: int, r: int) -> int:
    """c' - Unblinding operation (inverse commuting)"""
    r_inv = modulo_inverse(r, n)
    return (blinded_sig * r_inv) % n


## Redundancy Checking Function r
def redundancy_check(msg: int) -> bool:
    """r - Format verification"""
    return True


## Protocol:
# (1) Provider chooses x at random such that r(x) and forms c(x) and supplies c(x) to the signer
# (2) Signer signs c(x) by applying s' and returns s'(c(x)) to provider
# (3) Provider stiprs signed by application of c', yielding c'(s'(c(x))) = s'(x)
# (4) Anyone can check that the stripped matter s'(x) was formed by the signer by applying the signers public key s
#     and checking that r(s(s'(x)))





## Example Usage: 

# Variables:


# ----- Private to Signer -------
p, q = 5, 11   # large Primes (typically 2048+ bits)
n = p * q       # 55 # Used as Modulus
phi = (p-1) * (q-1)  # Euler's totient function # 40
e = 3  # Choose e such that e and phi are coprime (no common divisor except 1) (standard: 65537 (Prime) therefor very small change to not be coprime)
d = 27 # modulo_inverse(e, phi)    # Private signing key , Modular Inverse of e to mod phi
# -------------------------------

# ----- Made public by Signer ---
e = e           # public exponent (usally 65537)
n = n        # made public by Signer (n = p*q)
# -------------------------------

# ----- Private to Provider -----
r = 4# randomint(1, n-1)  # random Blinding Factor (must be co-prime with n) "Temporary private key"
msg = 13  # [ < n]                                 (must be co-prime with n)
# -------------------------------

if(not is_coprime(r,n) or not is_coprime(msg,n)):
    print("!!!Signature will fail: r and msg must be coprime with n!!!")

# User / Provider:
blinded = blind_message(msg, r)

# Signer:
signed = private_sign(blinded)

unblinded = unblind_signature(signed, r)
print(private_sign(msg))

check = public_verify(unblinded)

print(f"{msg=}, {blinded=}, {signed=}, {unblinded=}, {check=}")