#!/usr/bin/python3
from Cryptodome.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
pub_pem = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwGAKamKFesqyEfF3l3gS
H7VrkxAi62pLd+I4f/Atr/LhAcgQA1c9CIta2AQ1BJ3+rKHMHI1FJDDO2VwslKdV
qit1rCA41iAH0Nx4+T4KAQQLY/NxLbgFz9tTRM+kb53x1zVDUG/4IV8VIznMmSXG
j1YDhZUAaNnY6UfsBBKpPQ/9BP17ic8bjoyNFy7ryi7LUGhLtO3wfU2UbTYZrx9k
SsfT/r9OsK0B7Eoe4syY3/3nr/UplzWH4VMv57wfgy7j5mr1XKfmq8P2eqKH/8/p
GuCmJP6iXontxx7C3zjfBFBcFUbq+h/8TUgpFBbPV332kEaZ/du8wuo437CFrzSO
vQIDAQAB
-----END PUBLIC KEY-----
"""

priv_pem = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpgIBAAKCAQEAwGAKamKFesqyEfF3l3gSH7VrkxAi62pLd+I4f/Atr/LhAcgQ
A1c9CIta2AQ1BJ3+rKHMHI1FJDDO2VwslKdVqit1rCA41iAH0Nx4+T4KAQQLY/Nx
LbgFz9tTRM+kb53x1zVDUG/4IV8VIznMmSXGj1YDhZUAaNnY6UfsBBKpPQ/9BP17
ic8bjoyNFy7ryi7LUGhLtO3wfU2UbTYZrx9kSsfT/r9OsK0B7Eoe4syY3/3nr/Up
lzWH4VMv57wfgy7j5mr1XKfmq8P2eqKH/8/pGuCmJP6iXontxx7C3zjfBFBcFUbq
+h/8TUgpFBbPV332kEaZ/du8wuo437CFrzSOvQIDAQABAoIBAQCy0pPcAGkDk5ej
hkocyshOIV41/jH3k39DmU3b328YtzThaw83i8h4QNHZK0/9UsCByITrpYY39gbR
lhT6ufGvlWZ08h7jLDMXu1nYlgrGlvPfnVP/o6gDZ2Un+bxo5PEBk8lW5D5LBw+n
BvthAPRqGRJ9Ady3mok/kFOcFZyr3KuqQvN+SDN8O953pGpHTB06lyxqoaBCDxfs
r6oRUgWBSHHj8V+Z8U8oYYq4CwmCUi2j5CKyAE1lOlmOAN3ZQoYjiBs1uqWOon79
lMR8HFONu2Be7ygG2LYXS3vZ+IT5SNTt+V4eTEnbGntRgkGH4VlwZS2zFCK4Vq3V
CYgndtEhAoGBAOp77nENfOAB/TSLZldi6LiY4FkqQHYKzp17C3IHDZG/FJ5LHcLb
dteHHiq4kI7Ej0EHKDkRVHXon1G/I4wdgnXdYmPSX5KVfZrSfwX26IUqaewTnIhH
Nu0/Sm0OlURxC3/bWxVAsNOJSYoLMfRZdHi6OYjxs/3CLtTWC/dTsHhrAoGBANIG
9qTR7i2uC8mwYZmh18D/Uf60K5myRZITlaHWJHw8Gf/2P3fQ+M7ykMK9dOF5aYqQ
HhlXxsiYFgDiZEin3ZTn3CokBqiyoZtcwG1sYC5GzIcPVaJRroXTS39PZMbGcdCZ
eGhVT2PEewws13Z3SNsNFtt+Px6pFZhddG1XLv93AoGBAIgilae7PfHMFdaIzE0V
1qk90JrT5gLieVyC0H1OTPl+J5lTYR79Tb0J7GC/MOZChi0p25duUUv3V3AdeaTi
iRinBHWR8Pzon7jgVvD+jbaqjj6KkEmqluAc67fvTIgk3ZlIoFPxb/gQb8qef00v
Fmj1LWwtb+N29ruI3f+k7gKrAoGBAI6c5duzJOzlsuFoIE3m5I8Lj8zI4JZDxBPV
spQqyamGUg1JU31za49yjDN/3B7Ch5TsGVQSE0vgYYiGMZxYSBC1g/0la1Qfv7a0
O4HRxlmF/5lyIy7OEhiTCj/PVFnZJC2GGImX7AmNwBPbWw75HoKHl87BIfEa1SwZ
wVYBjksvAoGBAJHazTKGMZbi8p4rq9feUy4beLfySHVdmBDJquDEmJvzRtegzioX
OKfOEBbsktRfwKTzCVQrqY4P0t2jZB19fUkMBzrmwcsAzlOQVQQsHnqWVFNIj51l
+fSN3trj0Hd+KKAA5oXSzWNYrJ7fKDNIkU/f5rzvMlDM14GZ39dVELs+
-----END RSA PRIVATE KEY-----
"""

pub = RSA.import_key(pub_pem.strip())
priv = RSA.import_key(priv_pem.strip())
encryptor = PKCS1_OAEP.new(pub)
decryptor = PKCS1_OAEP.new(priv)
#setattr(priv, '_p', 11)
#setattr(priv, '_q', 13)
#setattr(priv, 'n', 11*13)
#priv.p = 11
#priv.q = 13
#priv.n = 11*13 # Break the private key

#encryptor = pkcs1_15.new(priv)
#decryptor = pkcs1_15.new(pub)
import binascii
from Cryptodome.Math.Numbers import Integer
def _encrypt(self, text_bytes):
    text = int(binascii.hexlify(text_bytes), 16)
    print('encrypt', text)
    i = _encrypt_int(self, text)
    print('encrypt got', i)
    res = binascii.unhexlify(hex(i)[2:])
    print('encrypt bytes {} -> {}'.format(len(text_bytes), len(res)))
    return res
def _decrypt(self, text_bytes):
    text = int(binascii.hexlify(text_bytes), 16)
    print('decrypt', text)
    i = _decrypt_int(self, text)
    print('decrypt got', i)
    res = binascii.unhexlify(hex(i)[2:])
    print('decrypt bytes {} -> {}'.format(len(text_bytes), len(res)))
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

def test(plain):
    h = binascii.hexlify(plain.encode('utf-8'))
    encoded = plain.encode('utf-8')
    encrypted = bytes()
    
    bytes_per_encrypt = pub.size_in_bytes()
    for cter in range(int(len(encoded)/bytes_per_encrypt)):
        encrypted += _encrypt(pub, encoded[cter*bytes_per_encrypt : (cter+1)*bytes_per_encrypt])
    left_bytes = len(encoded) % bytes_per_encrypt
    if left_bytes != 0:
        encrypted += _encrypt(pub, encoded[-left_bytes : ])
    
    ############## ENCRYPT DONE
    #print(encrypted)

    encoded = encrypted
    encrypted = bytes()
    bytes_per_encrypt = pub.size_in_bytes()
    for cter in range(int(len(encoded)/bytes_per_encrypt)):
        encrypted += _decrypt(priv, encoded[cter*bytes_per_encrypt : (cter+1)*bytes_per_encrypt])
    left_bytes = len(encoded) % bytes_per_encrypt
    if left_bytes != 0:
        encrypted += _decrypt(priv, encoded[-left_bytes : ])
    
    return encrypted.decode('utf-8')

def encryptDecryptBytes(func, key, bytes_to_convert):
    encoded = bytes_to_convert
    encrypted = bytes()
    
    bytes_per_encrypt = key.size_in_bytes()
    for cter in range(int(len(encoded)/bytes_per_encrypt)):
        encrypted += func(key, encoded[cter*bytes_per_encrypt : (cter+1)*bytes_per_encrypt])
    left_bytes = len(encoded) % bytes_per_encrypt
    if left_bytes != 0:
        encrypted += func(key, encoded[-left_bytes : ])
 
 
#i = 12345
#print(i) ; i = _encrypt_int(priv, i)
#print(i) ; i = _decrypt_int(priv, i)
#print(i) ; i = _decrypt_int(priv, i)
#print(i) ; i = _encrypt_int(priv, i)
#print(i) ;

assert(test("hello") == "hello")

#res = pub._encrypt("hello".encode('utf-8'))
#print(res)
#res = priv._decrypt(res).encode('utf-8')
#print(res)

#res = encryptor.encrypt("hellooooooooooooooooooooooooooooooooooo".encode('utf-8'))
#print(res)
#res = decryptor.decrypt(res).decode('utf-8')
#print(res)
#res = decryptor.encrypt("hellooooooooooooooooooooooooooooooooooo".encode('utf-8'))
#print(res)
#res = decryptor.decrypt(res).decode('utf-8')
#print(res)



#res = encryptor.sign("hello".encode('utf-8'))
#print(res)
#res = decryptor.verify(res).decode('utf-8')
#print(res)



