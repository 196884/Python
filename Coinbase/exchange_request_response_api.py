import sys
import ConfigParser
import json
import decimal
from decimal import Decimal
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python import log, util
from twisted.internet import protocol, reactor
from twisted.internet.defer import Deferred
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers
from order_book import MarketSide, Quote, BookPriceLevelAggregate

class CoinbaseRestClient:
    def __init__(self, appName, apiUri):
        log.msg('Initializing CoinbaseRestClient, appName[{0}], apiUri[{1}]'.format(appName, apiUri))
        self.appName = appName
        self.apiUri  = apiUri

    def _headers(self):
        return Headers({
            'Content-Type': ['application/json'],
            'Accept'      : ['application/json'],
            'User-Agent'  : [self.appName,     ]
        })

    def _responseHandler(self, response, cb, errorCb):
        if 200 != response.code:
            errorCb(response)
        else:
            body = readBody(response)
            body.addCallback(cb)
            body.addErrback(cb)
            return body
    
    def _getData(self, req, cb, errorCb):
        agent  = Agent(reactor)
        uri    = '{0}/{1}'.format(self.apiUri, req)
        d = agent.request('GET', uri, self._headers(), None)
        d.addCallback(lambda response: self._responseHandler(response, cb, errorCb))
        d.addErrback(errorCb)
        return d

    def getTime(self, cb, errorCb):
        return self._getData('time', cb, errorCb)

    def getCurrencies(self, cb, errorCb):
        return self._getData('currencies', cb, errorCb)

    def getProducts(self, cb, errorCb):
        return self._getData('products', cb, errorCb)

    def getTicker(self, product, cb, errorCb):
        return self._getData('products/{0}/ticker'.format(product), cb, errorCb)

    def getOrderBook(self, product, level, cb, errorCb):
        return self._getData('products/{0}/book?level={1}'.format(product, level), cb, errorCb)

class CoinbaseRequestResponseAPI:
    def __init__(self, config):
        self.clientName = config.get('coinbase', 'clientName')
        self.product    = config.get('coinbase', 'product')
        self.uri        = config.get('coinbase', 'restApiUri')
        self.log('initializing - clientName[{0}] product[{1}] uri[{2}]'.format(self.clientName, self.product, self.uri))
        self.restClient = CoinbaseRestClient(self.clientName, self.uri)

    def getTime(self, dataCb, errorCb):
        self.restClient.getTime(lambda d: self.onTime(dataCb, d), errorCb)

    def onTime(self, cb, d):
        dic = json.loads(d)
        cb(dic)

    def getCurrency(self, currency, dataCb, errorCb):
        self.restClient.getCurrencies(lambda d: self.onCurrencies(currency, dataCb, errorCb, d), errorCb)

    def onCurrencies(self, currency, dataCb, errorCb, d):
        ccyArray = json.loads(d)
        for ccyData in ccyArray:
            if ccyData.get('id', None) == currency:
                dataCb(ccyData)
                return None
        errorCb('no entry for {0} in the data returned by the exchange'.format(currency))

    def getProduct(self, product, dataCb, errorCb):
        self.restClient.getProducts(lambda d: self.onProducts(product, dataCb, errorCb, d), errorCb)

    def onProducts(self, product, dataCb, errorCb, d):
        prodArray = json.loads(d)
        for prodData in prodArray:
            if prodData.get('id', None) == product:
                dataCb(prodData)
                return None
        errorCb('no entry for {0} in the data returned by the exchange'.format(product))

    def getTicker(self, product, dataCb, errorCb):
        self.restClient.getTicker(product, lambda d: self.onTicker(product, dataCb, d), errorCb)

    def onTicker(self, product, dataCb, d):
        ticker = json.loads(d)
        dataCb(product, ticker)

    def getOrderBook(self, product, level, dataCb, errorCb):
        self.restClient.getOrderBook(product, level, lambda d: self.onOrderBook(product, level, dataCb, errorCb, d), errorCb)

    def onOrderBook(self, product, level, dataCb, errorCb, d):
        book = json.loads(d)
        if   1 == level:
            bid = book['bids'][0]
            ask = book['asks'][0]
            bk  = {
                MarketSide.BID: BookPriceLevelAggregate(Decimal(bid[0]), Decimal(bid[1]), bid[2]),
                MarketSide.ASK: BookPriceLevelAggregate(Decimal(ask[0]), Decimal(ask[1]), ask[2]),
            }
            dataCb(product, level, bk, book['sequence'])
            return
        elif 2 == level:
            bids = [ BookPriceLevelAggregate(Decimal(x[0]), Decimal(x[1]), x[2]) for x in book['bids'] ]
            asks = [ BookPriceLevelAggregate(Decimal(x[0]), Decimal(x[1]), x[2]) for x in book['asks'] ]
            bk = {
                MarketSide.BID: bids,
                MarketSide.ASK: asks,
            }
            dataCb(product, level, bk, book['sequence'])
            return
        elif 3 == level:
            bids = [ Quote(MarketSide.BID, Decimal(x[0]), Decimal(x[1]), x[2]) for x in book['bids'] ]
            asks = [ Quote(MarketSide.ASK, Decimal(x[0]), Decimal(x[1]), x[2]) for x in book['asks'] ]
            bk = {
                MarketSide.BID: bids,
                MarketSide.ASK: asks,
            }
            dataCb(product, level, bk, book['sequence'])
            return
        else:
            errorCb('onOrderBook - unexpected level {0}'.format(level))

    def log(self, msg):
        log.msg('CoinbaseRequestResponseAPI - {0}'.format(msg))

#################
## For testing ##
#################

class Tester:
    def __init__(self, config):
        self.api = CoinbaseRequestResponseAPI(config)

    def timeCb(self, time):
        print('timeCb - received time[{0}]'.format(time))
        print('iso: {0}'.format(time['iso']))
        reactor.stop()

    def currencyCb(self, ccyData):
        print('currencyCb - received currency data[{0}]'.format(ccyData))
        reactor.stop()

    def productCb(self, prodData):
        print('productCb - received product data[{0}]'.format(prodData))
        reactor.stop()

    def tickerCb(self, product, ticker):
        print('tickerCb - product[{0}] data[{1}]'.format(product, ticker))
        reactor.stop()

    def bookCb(self, product, level, book, sequence):
        print('bookCb - product[{0}] level[{1}] book[{2}] sequence[{3}]'.format(product, level, book, sequence))
        reactor.stop()

    def onError(self, data):
        print('onError - {0}'.format(data))
        reactor.stop()

    def first(self):
        #self.api.getTime(self.timeCb, self.onError)
        #self.api.getCurrency('BTC', self.currencyCb, self.onError)
        #self.api.getProduct('BTC-USD', self.productCb, self.onError)
        #self.api.getTicker('BTC-USD', self.tickerCb, self.onError)
        #self.api.getOrderBook('BTC-USD', 1, self.bookCb, self.onError)
        #self.api.getOrderBook('BTC-USD', 2, self.bookCb, self.onError)
        self.api.getOrderBook('BTC-USD', 3, self.bookCb, self.onError)

if __name__ == '__main__':
    if 2 != len(sys.argv):
        print('Expected unique argument (configuration file)')
    else:
        configFile = sys.argv[1]
        config = ConfigParser.RawConfigParser()
        config.read(configFile)
        tester = Tester(config)
        reactor.callWhenRunning(tester.first)
        reactor.run()
        

