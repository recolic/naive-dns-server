#!/usr/bin/python3
from Cryptodome.PublicKey import RSA
from Cryptodome.Math.Numbers import Integer
import binascii
def _encrypt(self, text_bytes):
    text = int(binascii.hexlify(text_bytes), 16)
    i = _encrypt_int(self, text)
    res = binascii.unhexlify(hex(i)[2:])
    return res
def _decrypt(self, text_bytes):
    text = int(binascii.hexlify(text_bytes), 16)
    i = _decrypt_int(self, text)
    res = binascii.unhexlify(hex(i)[2:])
    return res

def _encrypt_int(self, plaintext):
    if not 0 < plaintext < self._n:
        raise ValueError("Plaintext too large")
    return int(pow(Integer(plaintext), self._e, self._n))

def _decrypt_int(self, ciphertext):
    if not 0 < ciphertext < self._n:
        raise ValueError("Ciphertext too large")
    if not self.has_private():
        raise TypeError("This is not a private key")
    #return int(pow(Integer(ciphertext), self._d, self._n))

    # Blinded RSA decryption (to prevent timing attacks):
    # Step 1: Generate random secret blinding factor r,
    # such that 0 < r < n-1
    r = Integer.random_range(min_inclusive=1, max_exclusive=self._n)
    # Step 2: Compute c' = c * r**e mod n
    cp = Integer(ciphertext) * pow(r, self._e, self._n) % self._n
    # Step 3: Compute m' = c'**d mod n       (ordinary RSA decryption)
    m1 = pow(cp, self._d % (self._p - 1), self._p)
    m2 = pow(cp, self._d % (self._q - 1), self._q)
    h = m2 - m1
    while h < 0:
        h += self._q
    h = (h * self._u) % self._q
    mp = h * self._p + m1
    # Step 4: Compute m = m**(r-1) mod n
    result = (r.inverse(self._n) * mp) % self._n
    # Verify no faults occured
    if ciphertext != pow(result, self._e, self._n):
        raise ValueError("Fault detected in RSA decryption")
    return int(result)

def encryptDecryptBytes(func, key, bytes_to_convert):
    encoded = bytes_to_convert
    encrypted = bytes()
    
    bytes_per_encrypt = key.size_in_bytes()
    for cter in range(int(len(encoded)/bytes_per_encrypt)):
        encrypted += func(key, encoded[cter*bytes_per_encrypt : (cter+1)*bytes_per_encrypt])
    left_bytes = len(encoded) % bytes_per_encrypt
    if left_bytes != 0:
        encrypted += func(key, encoded[-left_bytes : ])

    return encrypted
