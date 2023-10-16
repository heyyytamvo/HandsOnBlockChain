import hashlib
import json
import time

class Block:
    def __init__(self, _id, _history):
        self.id = _id
        self.history = _history
        self.hashCode = None
        self.parent_hash = None
        self.miningTime = None
        
    def getHash(self):
        return self.hashCode

block_A = Block(1, 'Nelson likes cat')
block_B = Block(2, 'Marie likes dog')
block_C = Block(3, 'Sky hates dog')

class BlockChain():
    def __init__(self, _zeroDigits) -> None:
        self.BlockList=[]
        self.zeroDigits = _zeroDigits
        
    def getFirstBlock(self):
        return self.BlockList[0]
    
    def getLastBlock(self):
        return self.BlockList[len(self.BlockList) - 1]
    
    def addBlock(self, block, iterations):
        start_time = time.time()
        for i in range(iterations):
            nonce = str(i).encode('utf-8')
            hashedKey = hashlib.sha256(json.dumps(block.__dict__).encode('utf-8') + nonce).hexdigest()
            
            if hashedKey[0:self.zeroDigits] == ('0'* self.zeroDigits):
                block.hashCode = hashedKey
                
                if len(self.BlockList)==0:
                    block.parent_hash = None
                else:
                    block.parent_hash = self.getLastBlock().getHash()
                
                end_time = time.time()
                execution_time = end_time - start_time
                block.miningTime = round(execution_time, 4)
                self.BlockList.append(block)
                return
        
        print("Cannot add this block to the chain within ", iterations ," iterations")
                    
    
    def getAllBlock(self):
        for block in self.BlockList:
            print("Block ID: ", block.id)
            print("Block Hash Code: ", block.getHash())
            print("Block Parent Hash: ", block.parent_hash)
            print(f"This block takes {block.miningTime}s to find the Hashed Code")
            print()
            
    def validate(self):
        for i in range(len(self.BlockList)):
            currentBlock = self.BlockList[i]
            
            if currentBlock.parent_hash == None:
                continue
            
            parentBlock = self.BlockList[i - 1]
            if parentBlock.getHash() != currentBlock.parent_hash:
                print("Invalid")
                return
            
        print("Valid")
            
myBlockChain = BlockChain(5)
myBlockChain.addBlock(block_A, 10000000)
myBlockChain.addBlock(block_B, 10000000)
myBlockChain.addBlock(block_C, 10000000)

myBlockChain.getAllBlock()

    