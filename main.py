import time
import hashlib
import json

class Blockchain:
    def __init__(self):
        self.chain = [self.createGenesisBlock()]
        self.pendingTransactions = []
    
    def createGenesisBlock(self):
        return {
            "index": 1,
            "timestamp": time.time(),
            "nonce": 0,
            "hash": "hash",  # Placeholder, will be updated later
            "previousBlockHash": "0",  # Typically, the previous hash is "0" for the genesis block
        }
    
    def getLastBlock(self):
        return self.chain[-1]  # More Pythonic way to get the last block
    
    def generateHash(self):
        json_string = json.dumps(self.pendingTransactions)
        hash = ""  # Initialize hash
        nonce = 0
        
        # Loop until a valid hash is found
        while hash[0:3] != "000":
            nonce += 1
            block_data = (
                self.getLastBlock().get("previousBlockHash") +
                str(self.getLastBlock().get("timestamp")) +
                str(nonce) +  # Ensure nonce is a string
                json_string
            )
            
            # Generate the SHA-256 hash
            sha256_hash_object = hashlib.sha256(block_data.encode('utf-8'))
            hash = sha256_hash_object.hexdigest()
        
        return hash, nonce
    
    def createNewTransaction(self, amount, sender, recipient):
        newTransaction = {
            "amount": amount,
            "sender": sender,
            "recipient": recipient  # Fixed typo from "recepient" to "recipient"
        }
        self.pendingTransactions.append(newTransaction)
    
    def createNewBlock(self):
        timestamp = time.time()
        previousBlockHash = self.getLastBlock().get("hash")  # Use the hash of the last block
        hash, nonce = self.generateHash()
        transactions = self.pendingTransactions
        
        newBlock = {
            "index": len(self.chain) + 1,
            "timestamp": timestamp,
            "nonce": nonce,
            "hash": hash,
            "previousBlockHash": previousBlockHash,
        }
        
        self.chain.append(newBlock)
        self.pendingTransactions = []  # Clear pending transactions after mining

# Example usage
obj = Blockchain()
obj.createNewTransaction("100", "Marcus", "Thomas")
obj.createNewBlock()

print(f"Chain: {obj.chain}")
print(f"Pending Transactions: {obj.pendingTransactions}")
