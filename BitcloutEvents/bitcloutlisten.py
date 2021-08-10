import time
import requests
import json

endpoint = 'http://127.0.0.1:17001/'

def getChainHeight():
    response = requests.post(endpoint+'api/v1/node-info', json={})
    respdata = json.loads(response.text)
    chainheight = respdata['BitCloutStatus']['LatestBlockHeight']
    return chainheight

def getBlockInfo(height):
    # Call /api/v1/block to get details about a block passed to the function
    data = { 'Height':height, 'FullBlock':True }
    response = requests.post(endpoint+"/api/v1/block", json=data)

    # Return the JSON response
    respdata = json.loads(response.text)
    return respdata

def processBlock(height):
    print('new height:', height)

top = getChainHeight()
print('current block is ', top)

block = getBlockInfo(47207)
print(block - 1)
exit()
while True:
    newtop = getChainHeight()
    if newtop > top:
        top = newtop
        processBlock(top)
    else:
        print(".")
    time.sleep(1.0)