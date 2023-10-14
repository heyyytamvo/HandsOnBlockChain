# Chapter 1
## How do we verify the message
Given a message with the signature, we calculate the hash of the message and we decrypts the signature with public key. Then, we compare those two results: if they are the same, everything is well. Otherwise, either the message has been altered or the private key used to sign the message is different.

## Sign message
The file [verifyMessage.py](./verifyMessage.py) is used to sign the message "Nelson likes cat". 

## Verify but wrong

The file [falsify_message.py](./falsify_message.py) is used to verify the message "Nelson hates cat" with a different signature "Fake Signature" as below:

```python
message = b'Nelson hates cat'
signature = b'Fake Signature'

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
```
And here is the output:

```shell
(blockchain) (base) tamvo@Tams-MacBook-Air Blockchain % python3 falsify_message.py
Traceback (most recent call last):
  File "/Users/tamvo/Desktop/COS30049/Blockchain/falsify_message.py", line 15, in <module>
    public_key.verify(
  File "/Users/tamvo/Desktop/COS30049/Blockchain/blockchain/lib/python3.10/site-packages/cryptography/hazmat/backends/openssl/rsa.py", line 582, in verify
    _rsa_sig_verify(
  File "/Users/tamvo/Desktop/COS30049/Blockchain/blockchain/lib/python3.10/site-packages/cryptography/hazmat/backends/openssl/rsa.py", line 324, in _rsa_sig_verify
    raise InvalidSignature
cryptography.exceptions.InvalidSignature
```

## Verify true
The file [testTrueVerify.py](./testTrueVerify.py) is used to verify the message "Nelson likes cat" with the key taken from [verifyMessage.py](./verifyMessage.py) as below:

```python
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
```

After executing, nothing happens because the message and the signature match each others.

## Against cheating

Supposed that Nelson changes his history in block A from "Nelson likes cat" to "Nelson hates cat" in the file [againstCheating](./againstCheating.py)

```python
class Block:
    id = None
    history = None
    parent_id = None
    parent_hash = None
block_A = Block()
block_A.id = 1
block_A.history = 'Nelson likes cat'

block_B = Block()
block_B.id = 2
block_B.history = 'Marie likes dog'
block_B.parent_id = block_A.id
block_B.parent_hash = hashlib.sha256(json.dumps(block_A.__dict__).encode('utf-8')).hexdigest()

block_C = Block()
block_C.id = 3
block_C.history = 'Marie likes dog'
block_C.parent_id = block_B.id
block_C.parent_hash = hashlib.sha256(json.dumps(block_B.__dict__).encode('utf-8')).hexdigest()

print("Before changing, block A is encrypted as: ", block_B.parent_hash)
print("Before changing, block B is encrypted as: ", block_C.parent_hash)

block_A.history = 'Nelson hates cat'

block_B.parent_hash = hashlib.sha256(json.dumps(block_A.__dict__).encode('utf-8')).hexdigest()
block_C.parent_hash = hashlib.sha256(json.dumps(block_B.__dict__).encode('utf-8')).hexdigest()

print("After changing, block A is encrypted as: ", block_B.parent_hash)
print("After changing, block B is encrypted as: ", block_C.parent_hash)
```

Here is the output:

```shell
Before changing, block A is encrypted as:  69a1db9d3430aea08030058a6bd63788569f1fde05adceb1be6743538b03dadb
Before changing, block B is encrypted as:  ea6043f03881a1808cd073f65b73cdf246d6036d12bf236d18c532717ec05d06
After changing, block A is encrypted as:  00020490f78182785d6361c65290f6e1587f6e4591d8bab0d38e2df313086141
After changing, block B is encrypted as:  95e67747e67d6e37d2533734a6984d69695a6bec655c6d161224cd000b0f5fa8
```

Then, we have an issue existing: WE HAVE TO MODIFY THE REMAINING `parent_hash`.



