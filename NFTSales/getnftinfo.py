import requests
import json
from IPython.display import display
from PIL import Image
from datetime import datetime


endpoint = 'http://127.0.0.1:17001'

#Get latest header height from node-info endpoint (which is strangely a POST with no body. Why not GET?)
def getChainHeight():
    response = requests.post(endpoint+'/api/v1/node-info', json={})
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

def getPost(hash):
    data = {'PostHashHex':hash}
    response = requests.post(endpoint+'/api/v0/get-single-post',json=data)
    respdata = {}
    if response.status_code == 200:
        respdata = json.loads(response.text)
    else:
        print('Not Found!')
    return respdata

def showImages(post):
    imgurls = post['ImageURLs']
    if imgurls != None:                
        #print(post['Body'])
        for url in imgurls:
            print(url)            
        
            i = Image.open(requests.get(url, stream=True).raw)
            i.thumbnail((256,256))
            #display(i) 

def readTransactions(transactions):
    c = 0

    ret_nft_sells = []

    for tx in transactions:
        if tx['TransactionType'] == 'ACCEPT_NFT_BID':
            meta = tx['TransactionMetadata']
            
            buyerkey = ''
            sellerkey = ''
            for key in meta['AffectedPublicKeys']:
                uhash = key['PublicKeyBase58Check']
                if key['Metadata'] == 'BasicTransferOutput':
                    sellerkey = uhash
                else:
                    buyerkey = uhash
            nft = meta['AcceptNFTBidTxindexMetadata']
            nftposthash = nft['NFTPostHashHex']
            bid = nft['BidAmountNanos']
            serial = nft['SerialNumber']
            item = {
                "nftposthash" : nftposthash,
                "bid" : bid,
                "serial" : serial,
                "buyerkey" : buyerkey,
                "sellerkey" : sellerkey,
                "buyer" : getname(buyerkey),
                "seller" : getname(sellerkey)
            }
            ret_nft_sells.append(item)

            #print(nftposthash + ',' + str(block) + ',' + str(bid) + ',' + str(serial) + ',' + getname(buyerkey) + ',' + getname(sellerkey))
            #p = getPost(nftposthash)
            #showImages(p['PostFound'])
        c += 1
    return ret_nft_sells

def getname(hash):
    data = {'PublicKeyBase58Check':hash}
    response = requests.post(endpoint+"/api/v0/get-single-profile", json=data)
    respdata = {}

    if response.status_code == 200:
        respdata = json.loads(response.text)
        return respdata['Profile']['Username']
    else:
        return ''


top = getChainHeight()
#start = 46000
start = top - 15
counter = 0

f = open('nft_sells.csv', 'w')
f.write('post,bid,block,serial,buyer,seller,date\n')
f.close()

for block in range(start, top):
    print(block)
    info = getBlockInfo(block)

    timestamp = info['Header']['TstampSecs']
    dt_object = datetime.fromtimestamp(timestamp)
    print(str(dt_object))
    nfts = readTransactions(info['Transactions'])

    f = open('nft_sells.csv', 'a+')
    for nft in nfts:
        f.write(nft['nftposthash'] + ',' + 
            str(nft['bid']) + ',' + 
            str(block) + ',' + 
            str(nft['serial']) + ',' + 
            nft['buyer'] + ',' +
            nft['seller'] + ',' + 
            str(dt_object) + '\n')
    f.close()
    counter += 1

    if(counter> 10):
        break