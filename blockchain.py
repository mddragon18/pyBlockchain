import time
import hashlib
import json
class Blockchain:
    def __init__(self):
        self.chain=[self.createGenesisBlock()]
        self.pendingTransactions=[]
    
    def createGenesisBlock(self):
        return {
            "index":1,
            "timestamp":time.time(),
            "nonce":0,
            "hash":"hash",
            "previousBlockHash":"0",
        }
    
    def getLastBlock(self):
        return self.chain[len(self.chain)-1]
    
    def generateHash(self):
        json_string = json.dumps(self.pendingTransactions)
        hash=""
        nonce=0
        while(hash[0:3]!="000"):
            nonce+=1
            sha256_hash_object = hashlib.sha256((self.getLastBlock().get("previousBlockHash")+str(self.getLastBlock().get("timestamp"))+str(nonce)+json_string).encode('utf-8'))
            hash=sha256_hash_object.hexdigest()
        return hash,nonce
    
    def createNewTransaction(self,amount,sender,recepient):
        newTransaction = {"amount":amount,
                          "sender":sender,
                          "recepient":recepient}
        self.pendingTransactions.append(newTransaction)
    
    def createNewBlock(self):
        timestamp = time.time()
        previousBlockHash=self.getLastBlock().get("hash")
        hash,nonce=self.generateHash()
        transactions=self.pendingTransactions
        newBlock = {
            "index":(len(self.chain)+1),
            "timestamp":timestamp,
            "nonce":nonce,
            "hash":hash,
            "previousBlockHash":previousBlockHash,   
        }
        self.chain.append(newBlock)
        self.pendingTransactions=[]
    

obj = Blockchain()

obj.createNewTransaction("100","Marcus","Thomas")
obj.createNewTransaction("100","Marcus","Thomas")
obj.createNewBlock()
obj.createNewBlock()

print(f"chain : {obj.chain}")
print(f"Pending Transactions : {obj.pendingTransactions}")

