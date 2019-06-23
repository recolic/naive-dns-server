#!/usr/bin/python3
from Cryptodome.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
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

res = encryptor.encrypt("hello".encode('utf-8'))
print(res)
res = decryptor.decrypt(res).decode('utf-8')
print(res)


#key = RSA.generate(2048)
#pv_key_string = key.exportKey()
#with open ("private.pem", "w") as prv_file:
#    print("{}".format(pv_key_string.decode()), file=prv_file)
#
#pb_key_string = key.publickey().exportKey()
#with open ("public.pem", "w") as pub_file:
#    print("{}".format(pb_key_string.decode()), file=pub_file)



