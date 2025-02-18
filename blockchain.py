import time
import hashlib
import json
class Blockchain:
    def __init__(self):
        self.chain=[self.createGenesisBlock()]
        self.pendingTransactions=[]
    
    def createGenesisBlock(self):
        genesisBlock= {
            "index":1,
            "timestamp":time.time(),
            "transactions":[],
            "previousBlockHash":"0",
        }
        genesisBlock["hash"],genesisBlock["nonce"]=self.generateHash(genesisBlock["previousBlockHash"],genesisBlock["timestamp"],genesisBlock["transactions"])
        return genesisBlock
    
    def getLastBlock(self):
        return self.chain[-1]
    
    def generateHash(self,previousBlockHash,timestamp,transactions):
        nonce = 0
        while True:
            hash_input=f"{previousBlockHash}{timestamp}{transactions}{nonce}"
            hash=hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
            if hash[:3]=="000":
                return hash,nonce
            nonce+=1
    
    def createNewTransaction(self,amount,sender,recepient):
        newTransaction = {"amount":amount,
                          "sender":sender,
                          "recepient":recepient}
        self.pendingTransactions.append(newTransaction)
    
    def createNewBlock(self):
        previousBlock = self.getLastBlock()
        newBlock={
            "index":len(self.chain)+1,
            "timestamp":time.time(),
            "transactions":self.pendingTransactions,
            "previousBlockHash":previousBlock["hash"],
        }
        newBlock["hash"],newBlock["nonce"]=self.generateHash(newBlock["previousBlockHash"],newBlock["timestamp"],newBlock["transactions"])
        self.chain.append(newBlock)
        self.pendingTransactions=[]
    
    def printChain(self):
        for block in self.chain:
            print(json.dumps(block,indent=' '))
    

obj = Blockchain()

obj.createNewTransaction("100","Marcus","Thomas")
obj.createNewBlock()
obj.createNewTransaction("10","Alice","Bob")
obj.createNewBlock()
obj.printChain()


