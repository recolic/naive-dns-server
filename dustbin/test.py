#!/usr/bin/python3
import ctypes, base64

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
""".strip()

conf = """
SJTSDgLDB4YXF+dwuY/NFIvL8fHmwdsiMiH0183rhN102iy0qh/t/m+CGCtsEbOfnl8/VWEo
mOVW1IPgHx2vy54mmPXIx8Lry1hOAkQ+Lhe0SrQWTWNLsItKQytKmidYiz/pHwo3Q6nPIUBs
zimkT/uUePbCQW2VgT5k2fSJJXTWw51GvRcuTLygh3M73+CAfECKrVpkR9Y+5Lgup5ExjVF2
pmILDw0+zPx8eqZLmpEj4OqfsZHrR5brGiTLkzO5PbSDChB/DxeiJgr+4Y0RiSzthRovCIf5
gfWaR9iXEao6ijQ0/jvghfXXVsvghnvKXu5Izn/xtwQTPdkd9V97xNE3OhBKfF66TDvW594S
1yAKD2bgDCdGwNDmblTjw6DMqYPtmao49v/5yobk86cU+WK3RgCRNdpzJb73/i85BpS14GXw
L8Bu27vXvNyLuOUpD3LjO5OkdcKAbLetj37IPTCq2S2r8SaOajGzb5s2fZw01p+loFlTcC9j
fYNqSZmIAXh9gurKzqz81JJsL9iaJRlZ62Bl8j9WEmyCfFUpYutoBrfzaF02A+lvfySE9sKD
EoldYVteHj0HJg82deXZiLllCi/8d7dsFBvhrmenQkCv2dGT9ZXuI89DwPIY5pxDDN6x3vet
4pVz7jx4jkBIjtHL2kDYKMJW3t5DlcjKFTQeKLwhucXHOPojVQR655UEP1Joa0NbewfMs1eD
LlpjlPIirWwCM32LA2IOXb4Pdr2Ao8TNXJYcqrLkNwiYfqnMFSGkNykS7pu3iJt9LNft/abo
ztyBg/AuXjJdqIABwzHEdbyOStgix1zeBbkk2mdT1lmSlswc4Tnlmx13l/39sRk/kMOKh3u4
oOcD3bP8sH7YiApQqVziOGloVOYcKZ/8xhQoI3M7y+6rxiyBLTWGdWedb3QwXlUPQTlgo+v9
qxAAHCe/xeT1DQmcbmojxOgHSdwlCie/zm5c3penFv02vybAnASLQaABtBUCvP4oOxBqi2T0
JFZpOVpMOexWL7IJQNbc2DFACxjz4G+Mqqngy2mSaaiKzA/siu9fKCWDfivoeZGKuuEBDTSy
yXudf/L0gkZPumMwKUFbv0ZpfipT9Cv+fgOOwIg06fND7/JUW3fpuzXpCoII6fWuUiMdDgsM
XvXezRIHiQbeHC4utLAKwX7idygC9o8Lp6jtk6bIqbeeG7TRtUobc8OKa+W0pYFtzPcYiuYC
C2/sWCU6rgXHjVZdkqxPrQO76zSqVEOV8sHyO1Lu8zhL+s6e7bXqXI0dNPiCxK23I1pNVZ91
o+jz4pFyENQmyJF3y9QE8zVAQ5khX88QKKrlfL1UWd86Ele5q5g/QPjNOJ/PLqRSYcf20VGo
9TMdNDJM3rGRVJSCsqXXbWKpzWrX8ku7K4C0PiQIeeHUCyHfE7l1nLynqKtg5+5QJl+e4Sop
YkQZGst7/3+04I9F9w4x+4b75xkb6qO8pCFKV9Esqoaawc2BKJjgek6HgZIt/W/jD76R6I0Y
kwOK5bZwjl3kJUb/O0tpbQb6C6/BBU5XYrMrLDVRpKOLF7elYMppPdUIUbI3ooPLXyE4+z2D
oSL4E0lh4OqH2fP1V9NWgT6C5Ps9zd5Gs8bdE68w0GVqjGKl9gQJJ9XzSFQke4S8Zf1snY5y
jZJgBQsoCcHVaUdVcaibviko9uBP2lstvJc5b2LL1eJ84XIbArk=
""".strip().replace('\n', '')

func = ctypes.CDLL('./decrypt.so')
func.do_decrypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_size_t)]
func.do_decrypt.restype = ctypes.c_int

pub_pem_s = ctypes.c_char_p(pub_pem.encode('ascii'))
data_s = base64.b64decode(conf)
data_size = len(data_s)
data_s = ctypes.c_char_p(data_s)
output_data = ctypes.c_void_p()
output_data_size = ctypes.c_size_t()

return_val = func.do_decrypt(pub_pem_s, data_s, data_size, ctypes.pointer(output_data), ctypes.pointer(output_data_size))
ctypes.cast(output_data, ctypes.c_char_p)
if return_val != 0:
    print('Error: return_val is ' + str(return_val))

print(str(output_data))


exit(1)

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

import base64
def encrypt_private_key(a_message, private_key):
    encryptor = PKCS1_OAEP.new(private_key)
    encrypted_msg = encryptor.encrypt(a_message)
    print(encrypted_msg)
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)
    print(encoded_encrypted_msg)
    return encoded_encrypted_msg

def decrypt_public_key(encoded_encrypted_msg, public_key):
    encryptor = PKCS1_OAEP.new(public_key)
    decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
    print(decoded_encrypted_msg)
    decoded_decrypted_msg = encryptor.decrypt(decoded_encrypted_msg)
    print(decoded_decrypted_msg)
    #return decoded_decrypted_msg

pub = RSA.import_key(pub_pem.strip())
priv = RSA.import_key(priv_pem.strip())
encryptor = PKCS1_OAEP.new(pub)
decryptor = PKCS1_OAEP.new(priv)

res = encrypt_private_key("hello".encode('utf-8'), priv)
print(res)
res = decrypt_public_key(res, pub).decode('utf-8')
print(res)
exit(0)


#encryptor = pkcs1_15.new(priv)
#decryptor = pkcs1_15.new(pub)


res = decryptor.decrypt("hellooooooooooooooooooooooooooooooooooo".encode('utf-8'))
print(res)
res = encryptor.encrypt(res).decode('utf-8')
print(res)
#res = encryptor.sign("hello".encode('utf-8'))
#print(res)
#res = decryptor.verify(res).decode('utf-8')
#print(res)



