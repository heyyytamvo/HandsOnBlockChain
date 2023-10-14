from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

message = b'Nelson likes cat'
signature = b'\x9f\xf5=W\xad\xe4\xee\xe8\x1a\xb3\xc4ID\x99GN\xf8M!\x1b\x82\xbe\xe9\r\xb4\x1d\x12\xff\xb7\x00\x1b\xcb\x8e\xbb$,x\xdb\xa1X\xbb\xadI\xbd\xd8\x02\xcd\x10A\t\xd9<\x14\x12\xb3a\xcen\x85\xbd\x0eY\xed\xa1\r\xe3\xe0X\x8fE|,\xbf\xc1\xb7\xc9)\x80\x13~\xb6{\xe5\xc8B\xa3\xc6/\xd2\xc5\xe1!\xdc\xf3\x1c\x14EA\xe1^\x1ft\xd4\x06\x81\x1497\xbb\xfa\xd0\xa3A&Q\x9a\x15g`rL\xc3\xd4\xca\xd6\xda\x90\x1e'

with open("nelsonkey.pub", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend())

public_key.verify(
 signature,
 message,
 padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256())