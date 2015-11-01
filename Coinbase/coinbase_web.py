import ConfigParser
import requests
from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.application.service import Application
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python import log, util
from twisted.python.logfile import DailyLogFile
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
import sys
import json
from decimal import Decimal
import decimal

decimal.getcontext().prec = 20

def formatBookSideL3(bs):
    result = []
    quantity = 0
    price = None
    for [p, s, oid] in bs:
        pd = Decimal(p)
        sd = Decimal(s)
        if price != pd and price is not None:
            result.append((price, quantity))
        price = pd
        quantity = quantity + sd
    result.append((price, quantity))
    return result

def formatBookL3(book):
    bids = formatBookSideL3(book["bids"])
    asks = formatBookSideL3(book["asks"])
    for (p, q) in reversed(bids):
        print "{0}x{1}".format(p, q)
    print "***********TOB****************"
    for (p, q) in asks:
        print "{0}x{1}".format(p, q)

if __name__ == '__main__':
    api_url = 'http://api.exchange.coinbase.com/'
    product = "BTC-USD"
    print "PRODUCTS"
    print requests.get(api_url + 'products').json()
    print ""
    print "ORDER BOOK (LEVEL 1)"
    print requests.get(api_url + 'products/' + product + '/book', params = {'level':1}).json()
    print ""
    print "ORDER BOOK (LEVEL 2)"
    print requests.get(api_url + 'products/' + product + '/book', params = {'level':2}).json()
    print ""
    print "ORDER BOOK (LEVEL 3)"
    bookL3 = requests.get(api_url + 'products/' + product + '/book', params = {'level':3}).json()
    formatBookL3(bookL3)
    print bookL3
    print ""
    print "PRODUCT TICKER"
    print requests.get(api_url + 'products/' + product + '/ticker').json()
    print ""
    print "PRODUCT TRADES"
    print requests.get(api_url + 'products/' + product + '/trades').json()
    print ""
    print "PRODUCT STATS"
    print requests.get(api_url + 'products/' + product + '/stats').json()
    print ""
    print "CURRENCIES"
    print requests.get(api_url + 'currencies').json()
    print ""
    print "TIME"
    print requests.get(api_url + 'time').json()
    print ""

