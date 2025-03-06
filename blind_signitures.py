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

# ------ RSA Setup (Signer's Secrets) --------
# 1. Key Generation (Signer's Private Parameters)
p, q = 7907, 7919   # Secret primes (normally 2048+ bits in real implementations)
n = p * q       # Modulus for RSA operations (55)
phi = (p-1) * (q-1)  # Euler's totient (40) - needed for key generation
e = 65537  # Public exponent (typically 65537 in practice)
d = modulo_inverse(e, phi) # Private exponent: e⁻¹ mod phi (27 ≡ 3⁻¹ mod 40)
# --------------------------------------------


# ------ Public Key Disclosure ---------------
# 2. Signer Publishes Verification Key
e = e           # Public verification exponent
n = n           # Public modulus
# --------------------------------------------


# ------ Blind Signature Protocol ------------
# 3. Provider Prepares Message (Client Side)
r = 4           # Secret blinding factor (must be coprime with n)
msg = 123123        # Message to be signed (must be < n and coprime with n)


# Check: r and msg must both be coprime with n for math to work
if not is_coprime(r,n) or not is_coprime(msg,n):
    print("!!! Signature will fail: r and msg must be coprime with n !!!")
# --------------------------------------------

# 4. Message Blinding (Client Side)
#    msg' = (msg * rᵉ) mod n (hides message from signer)
blinded = blind_message(msg, r)  


# 5. Blind Signing (Signer Side)
#    s' = (msg')ᵈ mod n (signer only sees blinded message)
signed = private_sign(blinded)  

# 6. Signature Unblinding (Client Side)
#    s = s' * r⁻¹ mod n (removes blinding factor)
unblinded = unblind_signature(signed, r)  

# 7. Verification Check (Can Be Done by Anyone)
#    Verifies that sᵉ ≡ msg mod n (using public exponent)
check = public_verify(unblinded)  

# Direct signing without blinding for comparison
direct_signature = private_sign(msg)  

print(f"""
Blind Signature Process:
{msg=} (original message)
{blinded=} (blinded message)
{signed=} (blind-signed message)
{unblinded=} (unblinded signature)
{direct_signature=} (direct signature for comparison)
{check=} (verification result)
""")