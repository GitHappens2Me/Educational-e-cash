from helper import modulo_inverse, is_coprime, is_moduloinverse
from random import randint
import hashlib

## Toy Example of Diffie-Hellman Blind Signatures as described in "https://cypherpunks.venona.com/date/1996/03/msg01848.html" by David Wagner

def prepare_message(x: str) -> int:
    """Erstellt y = x | hash(x) als Gruppen-Element"""
    h = hashlib.sha3_256(x.encode()).digest().hex()
    y_bytes = f"{x}:{h}".encode()
    return int.from_bytes(y_bytes, "big") % p

## Signing Function s'
## Only known to the Signer (Mint)
## used to sign the *blinded* Message
def private_sign(blinded: int) -> int:
    """Bank signiert die geblindete Nachricht"""
    return pow(blinded, k, p)  # (y·g^b)^k mod p

## publicly known
def verify(x: str, sig: int) -> bool:
    """Bank verifiziert Signatur"""
    y = prepare_message(x)
    return sig == pow(y, k, p)  # Prüfe y^k ≡ sig mod p

## Commuting (Blinding-) Function 
## Only known to the Provider (User)
def blind_message(y: int, b: int) -> int:
    """Blinding-Operation mit Zufallsfaktor b"""
    return (y * pow(g, b, p)) % p  # y·g^b mod p

## And its inverse c'
## Only known to the Provider (User)
def unblind_signature(signed: int, b: int) -> int:
    """Entfernt Blinding-Faktor"""
    r_inv = pow(g_k, -b, p)  # (g^k)^-b = g^{-kb} mod p
    return (signed * r_inv) % p  # y^k mod p


## Redundancy Checking Function r
def redundancy_check(msg: int) -> bool:
    """r - Format verification"""
    return True



## Example Usage: 

# ------ Public Parameters  ------------------
# 2. Signer Publishes Verification Key
p = 7   # Prime (normally 2048+ bits in real implementations)
g = 2       # Generator der Gruppe
# --------------------------------------------

# ------ Diffie Hellman Setup (Signer's Secrets) --------
k = 123142           # Banks private Key
# --------------------------------------------

g_k = pow(g, k, p)  # Banks Public Key

# ------ Blind Signature Protocol ------------
# 3. Provider Prepares Message (Client Side)
b = 25         # Client Private Key / Blinding factor
msg = "Cashu123123123"       # Message to be signed (must be < n and coprime with n)




# --------------------------------------------

# 1. Prepare Message (Client Side)
y = prepare_message(msg)  

# 2. Blind Message
blinded = blind_message(y, b)

# 3. Blind Signing (Signer Side)
signed = private_sign(blinded)  

# 4. Signature Unblinding (Client Side)
unblinded = unblind_signature(signed, b)  

# 7. Verification Check (Done by Bank)
check = verify(msg, unblinded)  

# Direct signing without blinding for comparison
direct_signature = private_sign(prepare_message(msg))  

print(f"""
Blind Signature Process:
{msg=} (original message)
{blinded=} (blinded message)
{signed=} (blind-signed message)
{unblinded=} (unblinded signature)
{direct_signature=} (direct signature for comparison)
{check=} (verification result)
""")