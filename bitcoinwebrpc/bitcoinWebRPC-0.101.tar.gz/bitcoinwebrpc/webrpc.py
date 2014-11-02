"""
web rpc
"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_jsonrpc import JSONRPC
import bitcoin
from json_proxy import RawProxy
import os

# Flask application
app = Flask(__name__)
Bootstrap(app)

# Flask-JSONRPC
#jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)
jsonrpc = JSONRPC(app, '/test', enable_web_browsable_api=True)

#bitcoin rpc , reads conf automatically
rp = RawProxy()

@jsonrpc.method('App.index')
def index():
    getinfo = str(rp._call('getinfo'))
    getbalance = str(rp._call('getbalance'))
    listaddressgroupings = str(rp._call('listaddressgroupings'))
    listreceivedbyaddress = str(rp._call('listreceivedbyaddress'))
    getpeerinfo = str(rp._call('getpeerinfo'))

    return {'message':'Nxt Bridge JSON-RPC ', 'getinfo': getinfo ,\
            'getbalance':getbalance, 'listaddressgroupings':listaddressgroupings, \
            'listreceivedbyaddress' :listreceivedbyaddress,'getpeerinfo':getpeerinfo
    }

@app.route('/')
def main():
    s = ""
    r = rp._call('getinfo')
    s += str(r['balance'])
    getinfo = str(rp._call('getinfo'))
    getbalance = str(rp._call('getbalance'))
    listaddressgroupings = str(rp._call('listaddressgroupings'))
    listreceivedbyaddress = str(rp._call('listreceivedbyaddress'))
    getpeerinfo = str(rp._call('getpeerinfo'))

    return render_template('info.html', getinfo=getinfo,getbalance=getbalance,listaddressgroupings=listaddressgroupings, listreceivedbyaddress=listreceivedbyaddress, getpeerinfo=getpeerinfo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
