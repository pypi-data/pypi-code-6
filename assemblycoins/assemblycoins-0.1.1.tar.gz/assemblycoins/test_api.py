import requests
import databases as db
import main
import addresses
import json

#test connection to colordb
def test_colordb_connected():
  a=db.dbexecute("SELECT * FROM meta;",True)
  print "COLOR DB NOT RESPONDING"
  assert len(a)>0

#test that color_db is up to date, at least according to meta
def test_meta_lastblockdone():
  blockchain_blockcount=requests.get("https://blockchain.info/q/getblockcount").content
  lastblockdone=db.dbexecute("SELECT * FROM meta;",True)
  try:
    lastblockdone=lastblockdone[0][0]
  except:
    lastblockdone=-1
  print "Color DB is not up to date, stuck at "+str(lastblockdone)+" out of "+str(blockchain_blockcount)
  assert int(lastblockdone)==int(blockchain_blockcount)

#TEST READING MESSAGES IN BLOCKCHAIN
def test_address_messages():
  found=addresses.read_opreturns_sent_by_address("1N8onLuitcQR9V3HB9QSARyFV6hwxA99Sx")
  should_be='{"name": "pillars", "desc": "one small step", "total": 52352}'
  assert found==should_be

#TEST KNOWN PUBLIC ADDRESS
def test_public_lookup():
  public_address="1CEyiC8DXT6TS3d9iSDnXRBtwyPuVGRa9P"
  url="https://coins.assembly.com/v1/addresses/"+str(public_address)
  should_be='{"public_address": "1CEyiC8DXT6TS3d9iSDnXRBtwyPuVGRa9P", "assets": [{"quantity": 10000, "color_address": "3N2bUx2XCWBfXzNd3YiDpFVAHQtSi1Yj5w"}]}'
  data=requests.get(url).content
  assert str(data)==should_be

#TEST A KNOWN COLOR ADDRESS
def test_color_lookup():
  color_address="3EKq4ecPqg33gzVkd4KaWe8oicVTkG1XUd"
  data=requests.get("https://coins.assembly.com/v1/colors/"+str(color_address)).content
  should_be='{"owners": [{"quantity": 1337, "public_address": "14vce6XiQzJ51cTKU1Dsj1X48hSdCTCq6Y"}], "color_address": "3EKq4ecPqg33gzVkd4KaWe8oicVTkG1XUd"}'
  assert str(data)==should_be

#Test a KNOWN TRANSACTION
def test_tx_lookup():
  url="https://coins.assembly.com/v1/transactions/88b73f03d6c594dd2e328a140a189533de52f97dccada45811554fbc6df7d802"
  data=requests.get(url).content
  should_be='{"outputs": [{"color_amount": 1337, "color_address": "3EKq4ecPqg33gzVkd4KaWe8oicVTkG1XUd", "destination_address": "14vce6XiQzJ51cTKU1Dsj1X48hSdCTCq6Y", "blockmade": 321435, "spent_at_txhash": "", "txhash_index": "88b73f03d6c594dd2e328a140a189533de52f97dccada45811554fbc6df7d802:0", "btc": 601, "spent": false, "txhash": "88b73f03d6c594dd2e328a140a189533de52f97dccada45811554fbc6df7d802", "blockspent": null, "previous_input": "source:14vce6XiQzJ51cTKU1Dsj1X48hSdCTCq6Y"}]}'
  assert data==should_be

#TEST 'PREPARE NEW COIN'
def test_prepare():
  url="https://coins.assembly.com/v1/colors/prepare"
  payload='{"issued_amount": 100, "description": "another test", "coin_name": "baltimore", "email": "afasd"}'
  headers = {'content-type': 'application/json'}
  response=requests.post(url, data=payload, headers=headers)
  print response.content
  should_be='{"name": "baltimore", "issuing_private_key": "5JsA268SaN3VrjnPM3m46JxE7mqibfYTD6Gacbhci17FYSuTUUc", "issuing_public_address": "1HRUD9KXmu7etUQPfYW7rnRrFfAzPq2sUj", "minting_fee": "0.00043606"}'
  jsonresponse=json.loads(response.content)
  db.dbexecute("delete from addresses * where coin_name='baltimore';", False)
  assert jsonresponse['name']=="baltimore" and float(jsonresponse['minting_fee'])>0

#test for colors of unknown origin
def test_unknown():
  response=db.dbexecute("select * from outputs where color_address='unknown' and spent='false';",True)
  assert len(response)==0
