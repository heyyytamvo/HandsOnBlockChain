import hashlib
import json
class Block:
    id = None
    history = None
    parent_id = None
    parent_id = None


block_D = Block()
block_D.id = 4
block_D.history = 'Sky loves turtle'
block_D.parent_id = 3


block_serialized = json.dumps(block_D.__dict__).encode('utf-8')
print(block_serialized)
