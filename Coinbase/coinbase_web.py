import sys
from twisted.internet import reactor

def stop(msg = ""):
    if len(msg) > 0:
        suffix = " [{0}]".format(msg)
    else:
        suffix = ""
    print "stop - stopping reactor{0}".format(suffix)
    reactor.stop()

def started():
    print "started - reactor is running"
    stop("finished")

def start_1(configFile):
    reactor.callWhenRunning(started)
    reactor.run()

######################################

from pprint import pformat
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers
from twisted.internet.protocol import Protocol

def cbBody(body):
    print 'Body: {0}'.format(body)

def onBookL1Data(data):
    print "onBookL1Data"
    print data
    print 'Response version: {0}'.format(data.version)
    print 'Response code:    {0}'.format(data.code)
    print 'Response phrase:  {0}'.format(data.phrase)
    print 'Response headers: {0}'.format(pformat(list(data.headers.getAllRawHeaders())))
    body = readBody(data)
    body.addCallback(cbBody)
    return body

def shutdown(x):
    print "shutdown"
    reactor.stop()

class CoinbaseRestClient:
    def __init__(self, appName, apiUri):
        self.appName = appName
        self.apiUri  = apiUri

    def _headers(self):
        return Headers({
            'Content-Type': ['application/json'],
            'Accept'      : ['application/json'],
            'User-Agent'  : [self.appName]
        })

    def _responseHandler(self, response, cb, errorCb):
        if 200 != response.code:
            errorCb(response)
        else:
            body = readBody(response)
            body.addCallback(cb)
            return body
    
    def _getData(self, req, cb, errorCb):
        agent = Agent(reactor)
        d = agent.request('GET', '{0}/{1}'.format(self.apiUri, req), self._headers(), None)
        d.addCallback(lambda response: self._responseHandler(response, cb, errorCb))
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
        
def printBody(body):
    print 'Received body:'
    print body

def onError(x):
    print "onError - aborting"
    reactor.stop()

def start_2(configFile):
    crc = CoinbaseRestClient('coinbase-client', 'https://api.exchange.coinbase.com')
    d   = crc.getTime(printBody, onError)
    e   = crc.getCurrencies(printBody, onError)
    f   = crc.getProducts(printBody, onError)
    g   = crc.getTicker("BTC-USD", printBody, onError)
    h   = crc.getOrderBook("BTC-USD", 2, printBody, onError)

    reactor.run()

    agent = Agent(reactor)
    print vars(agent)
    d = agent.request(
        'GET', 
        'https://api.exchange.coinbase.com/time',
        Headers({'Content-Type': ['application/json'], 'Accept': ['application/json'], 'User-Agent': ['coinbase-client']}),
        None
    )
    d.addCallback(onBookL1Data)
    reactor.run()

if __name__ == '__main__':
    if 2 != len(sys.argv):
        print "Expected unique argument (configuration file)"
    else:
        configFile = sys.argv[1]
        start_2(sys.argv[1])

