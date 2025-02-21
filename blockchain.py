import time
import hashlib
import json
from flask import Flask,jsonify,request
from flask_cors import CORS

class Blockchain:
    def __init__(self):                                 
        self.chain=[]
        self.pendingTransactions=[]
        self.createNewBlock(nonce=1,previousHash="0")               # Creates the genesis block with a nonce 1 , there is no previous block
    
    def getLastBlock(self):                                        # Used to fetch the previous block in the chain
        return self.chain[-1]
    
    def nonceOfWork(self,previousNonce):                            # Used to calculate the proof of work , depends on previousNonce makes it more secure
        newNonce = 0
        while True:
            nowHash=(hashlib.sha256(str(newNonce**2 - previousNonce**2).encode()).hexdigest())
            if nowHash[:3]=="000":
                return newNonce
            newNonce+=1
        
    
    def hash(self,block):                                           #Pass the entire block to calculate its hash.
        encodedBlock=(json.dumps(block,sort_keys=True)).encode()
        return hashlib.sha256(encodedBlock).hexdigest()
    
    
    
    def createNewTransaction(self,amount,sender,recipient):         
        newTransaction = {"amount":amount,
                          "sender":sender,
                          "recipient":recipient}
        self.pendingTransactions.append(newTransaction)
        
    
    def createNewBlock(self,nonce,previousHash):    # nonce and previousHash are provided in mineBlock() to keep createNewBlock() independent and previousHash is calculated only when it is required(i.e creating the next block).
        newBlock={
            "index":len(self.chain)+1,
            "timestamp":time.time(),
            "transactions":self.pendingTransactions,
            "nonce":nonce,
            "previousBlockHash":previousHash,
        }
        self.chain.append(newBlock)
        self.pendingTransactions=[]
        
    def mineBlock(self):                            #Self explanatory 
        previousBlock=self.getLastBlock()
        previousHash=self.hash(previousBlock)
        previousNonce=previousBlock["nonce"]
        nonce=self.nonceOfWork(previousNonce)
        self.createNewBlock(nonce,previousHash)
        
        
    def validateChain(self):
        previousBlock=self.chain[0]
        blockIndex=1
        
        while blockIndex < len(self.chain):
            block=self.chain[blockIndex]
            if block["previousBlockHash"]!=self.hash(previousBlock):            #Compares the previous hash stored in current block with livetime hash of the previousBlock to maintain consistency of the block , if tampered with , returns False
                return False
            
            nonce=block["nonce"]
            previousNonce=previousBlock["nonce"]
            hash_op=hashlib.sha256(str(nonce**2 - previousNonce**2).encode()).hexdigest()   #Extra layer of security to ensure the POW(or i call it the nonceOfWork) is valid
            if hash_op[:3]!="000":
                return False
            
            previousBlock=block
            blockIndex+=1
        
        return True
            
        
    def printChain(self):
        return self.chain
    
obj = Blockchain()
app=Flask(__name__)
CORS(app)

@app.route('/get-chain',methods=['GET'])
def getChain():
    return jsonify(obj.printChain())

@app.route('/mine-block',methods=['POST'])
def mine():
    obj.mineBlock()
    return jsonify({'message':'Block mined succesfully','chain':obj.chain})

@app.route('/create-tx',methods=['POST'])
def createTx():
    data=request.json
    sender=data.get('sender')
    recipient=data.get('recipient')
    amount=data.get('amount')
    if not sender or not recipient or not amount:
        return jsonify({"error":"Missing transaction data"})
    obj.createNewTransaction(amount,sender,recipient)
    return jsonify({"message":"transaction added successfully","pendingTransactions":obj.pendingTransactions})

    






app.run(debug=True)

