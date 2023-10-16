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

Supposed that Nelson changes his history in block A from "Nelson likes cat" to "Nelson hates cat" in the file [againstCheating.py](./againstCheating.py)

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

Now you need to have a fundamental for cryptography, this section will not be covered in here.

## Proof of work
So, blockchain will be a append-only database. Each block will reference its parent hash as below:

```python
import hashlib
import json
class Block:
    def __init__(self, _id, _history, Parent):
        if Parent:
            self.parent_id = Parent.id
            self.parent_hash = Parent.getHash()
        else:
            self.parent_id = None
            self.parent_hash = None
        self.id = _id
        self.history = _history
        
    def getHash(self):
        return hashlib.sha256(json.dumps(self.__dict__).encode('utf-8')).hexdigest()

block_A = Block(1, 'Nelson likes cat', None)
block_B = Block(2, 'Marie likes dog', block_A)
block_C = Block(3, 'Sky hates dog', block_B)
```

Here is what is going on under the hood:

```shell
Block A
Hash Code:  331ea9e6ecbe8cec7b281903103da42ca40377c7f2220712f0875ef4b786b061
Parent Hash:  None

Block B
Hash Code:  63d31121c69423ec2f56f0f86886b69d1aa2377a80833ecb16c46a48d681d02b
Parent Hash:  331ea9e6ecbe8cec7b281903103da42ca40377c7f2220712f0875ef4b786b061

Block C
Hash Code:  178d66fa587f3341cb46ef88b5fa78dd7579e3265f11787097fed609f4e37c94
Parent Hash:  63d31121c69423ec2f56f0f86886b69d1aa2377a80833ecb16c46a48d681d02b
```

Now we create a class called `BlockChain` as below:

```python
class BlockChain():
    def __init__(self) -> None:
        self.BlockList=[]
        
    def getFirstBlock(self):
        return self.BlockList[0]
    
    def getLastBlock(self):
        return self.BlockList[len(self.BlockList) - 1]
    
    def addBlock(self, block):
        self.BlockList.append(block)
    
    def getAllBlock(self):
        for block in self.BlockList:
            print("Block ID: ", block.id)
            print("Block Hash Code: ", block.getHash())
            print("Block Parent Hash: ", block.parent_hash)
            print()
```

Next, we create our first blockchain:

```python
myBlockChain = BlockChain()
myBlockChain.addBlock(block_A)
myBlockChain.addBlock(block_B)
myBlockChain.addBlock(block_C)
```

Suppose someone would like to access `block_A` and modify its content, they just simply perform this:

```python
myBlockChain.BlockList[1].history = 'Nelson loves cat'
```

The attacker just modify the content from **Nelson hates cat** to **Nelson loves cat**, how will we prevent it? That's when the function `Valid()` exists to check the hashing code inside the `BlockChain` class:

```python
class BlockChain():
    #####......
            
    def validate(self):
        for i in range(len(self.BlockList)):
            currentBlock = self.BlockList[i]
            
            if currentBlock.parent_id == None:
                continue
            
            parentBlock = self.BlockList[i - 1]
            if parentBlock.getHash() != currentBlock.parent_hash:
                print("Invalid")
                return
        
        print("Valid")


myBlockChain.BlockList[1].history = 'Nelson loves cat'
myBlockChain.validate()
```

Here is the output: Invalid.

But there are a drawback that need to be discussed further: The attacker will perform the hashing from the begining as below:

```python
myBlockChain.BlockList[0].history = 'Nelson loves cat'

for i in range(len(myBlockChain.BlockList)):
    currentBlock = myBlockChain.BlockList[i]
    if currentBlock.parent_id == None:
        continue
            
    parentBlock = myBlockChain.BlockList[i - 1]
    currentBlock.parent_id = parentBlock.id
    currentBlock.parent_hash = parentBlock.getHash()
    
myBlockChain.validate()
```

The output will be Valid. Instead of allowing the 'user' to append a block to our blockchain without any conditions, a block is only appended when its hashing code beginning with n 0's. For example, our block A's hashing code is a string like this: `331ea9e6ecbe8cec7b281903103da42ca40377c7f2220712f0875ef4b786b061`, instead, we want its hashing code looks like this: `000000....` or `000000000....`. So, the number of the first 0's digits will be the level of difficulty: more 0's, more difficult. 

We need to modify our code, for the `Block` class, it shoud not perform calculate the hash result. You can find the full source code at [proofOfWork.py](./proofOfWork.py). The attacker can perform hashing from the beginning, but the more the 0's digits, the more difficulties.

Here is an example output in the file:

```shell
Block ID:  1
Block Hash Code:  0000ae268c2207aa1f9119403def4207ff1cbaeb064aea2bd92b99db75c374d3
Block Parent Hash:  None
This block takes 0.4812s to find the Hashed Code

Block ID:  2
Block Hash Code:  000058b2f870cc7b99ccdd7bda4f35b1b5ac4fc57713aadc11175cfe12684d19
Block Parent Hash:  0000ae268c2207aa1f9119403def4207ff1cbaeb064aea2bd92b99db75c374d3
This block takes 0.3541s to find the Hashed Code

Block ID:  3
Block Hash Code:  0000f880d8aed5db1b1f010fce1bb1628e9f4b399a5378e011cff558d7a00323
Block Parent Hash:  000058b2f870cc7b99ccdd7bda4f35b1b5ac4fc57713aadc11175cfe12684d19
This block takes 0.0718s to find the Hashed Code
```
Or this:

```shell
Block ID:  1
Block Hash Code:  00000f841d3d1e65eb6f9d7ffcfc1bf99e6c9a990640e047cb6f3150e0953da4
Block Parent Hash:  None
This block takes 4.066s to find the Hashed Code

Block ID:  2
Block Hash Code:  000007fc8440e339705e6c861afd0c5efca856de47a9d1f5ecb06242a4a48955
Block Parent Hash:  00000f841d3d1e65eb6f9d7ffcfc1bf99e6c9a990640e047cb6f3150e0953da4
This block takes 1.111s to find the Hashed Code

Block ID:  3
Block Hash Code:  00000cd8556e8c4e870313c54952c9cc1bac78b0954c578836c367a2f5215cf4
Block Parent Hash:  000007fc8440e339705e6c861afd0c5efca856de47a9d1f5ecb06242a4a48955
This block takes 0.5249s to find the Hashed Code
```




