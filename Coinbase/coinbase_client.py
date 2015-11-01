import sys
import ConfigParser
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python import log, util
from twisted.internet import reactor
#from pprint import pformat
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers
#from twisted.internet.protocol import Protocol

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
        log.msg('Initializing CoinbaseRestClient, appName[{0}], apiUri[{1}]'.format(appName, apiUri))
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

def myFloEmit(self, eventDict):
    text = log.textFromEventDict(eventDict)
    if text is None:
        return
    self.timeFormat = "%Y%m%d-%H:%M:%S.%f %z"
    timeStr = self.formatTime(eventDict["time"])
    util.untilConcludes(self.write, timeStr + " " + text + "\n")
    util.untilConcludes(self.flush)

class CoinbaseClient:
    def __init__(self, config):
        self.restClient = CoinbaseRestClient(config.get('coinbase', 'clientName'), config.get('coinbase', 'restApiUri'))
        self.time       = None
        reactor.callWhenRunning(self.whenRunning)

    def log(self, msg):
        log.msg('CoinbaseClient - {0}'.format(msg))

    def whenRunning(self):
        self.log('reactor running')
        # The order is as follows:
        # 1. we get the time (to make sure the server is up)
        # 2. we get the products (to make sure the expected product is there, and check parameters)
        self.restClient.getTime(self.onTime, self.onRestClientError)

    def onTime(self, data):
        self.log('onTime: {0}'.format(data))
        self.restClient.getProducts(self.onProducts, self.onRestClientError)

    def onProducts(self, data):
        self.log('onProducts: {0}'.format(data))
        self.stop()

    def onRestClientError(self, x):
        self.log('onRestClientError[{0}]'.format(x))
        self.log('aborting')
        self.stop()

    def run(self):
        reactor.run()

    def stop(self):
        reactor.stop()



def start(config):
    crc = CoinbaseRestClient(config.get('coinbase', 'clientName'), config.get('coinbase', 'restApiUri'))
    d   = crc.getTime(printBody, onError)
    e   = crc.getCurrencies(printBody, onError)
    f   = crc.getProducts(printBody, onError)
    g   = crc.getTicker("BTC-USD", printBody, onError)
    h   = crc.getOrderBook("BTC-USD", 2, printBody, onError)
    reactor.run()

if __name__ == '__main__':
    if 2 != len(sys.argv):
        print "Expected unique argument (configuration file)"
    else:
        configFile = sys.argv[1]
        config = ConfigParser.RawConfigParser()
        config.read(configFile)
        clientName  = config.get("coinbase", "clientName")
        loggingFile = config.get("coinbase", "logFile")
        print "{0} - logging to '{1}'".format(clientName, loggingFile)
        log.FileLogObserver.emit = myFloEmit
        log.startLogging(open(loggingFile, 'w'))
        client = CoinbaseClient(config)
        client.run()
