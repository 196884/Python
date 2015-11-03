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
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
from enums import defEnum
from order_book import OrderBookSide, BookPriceLevel, Quote

ClientState = defEnum( 
    'INITIALIZING', 
    'WAITING_FOR_BOOK_SNAPSHOT',
    'INITIALIZING_BOOK',
    'RUNNING',
    'EXITING'
)

ServiceCommand = defEnum(
    'EXIT'
)

FeedHandlerState = defEnum('INACTIVE', 'BUFFERING', 'PROCESSING', 'DATALOSS')

class IMarketDataFeedHandlerCB:
    def onFeedDataloss(self):
        pass

    def onFeedError(self, error):
        pass

    def onFeedMsgOpen(self, quote):
        pass

    def onFeedMsgDone(self, quote):
        pass

    def onFeedMsgMatch(self, match):
        pass

    def onFeedMsgChange(self, change):
        pass

class CoinbaseMarketDataFeedHandler:
    """
    Mostly in charge of buffering messages pre-initial snapshot,
    then checking the sequence numbers, doing data decoding (object creation)
    and calling the right callbacks

    cb must implement IMarketDataFeedHandlerCB
    """
    def __init__(self, cb):
        self.cb               = cb
        self.state            = FeedHandlerState.INACTIVE
        self.bufferedMessages = []
        self.expSeqNum        = None

    def __str__(self):
        return 'CoinbaseMarketDataHandler[{0}, bufferedMessages: {1}, expSeqNum: {2}]'.format(self.state, len(self.bufferedMessages), self.expSeqNum)

    def startBuffering(self):
        self.state = FeedHandlerState.BUFFERING

    def inactivate(self):
        self.state = FeedHandlerState.INACTIVE

    def onDataloss(self, sequence):
        self.state = FeedHandlerState.DATALOSS
        self.cb.onFeedDataloss()

    def onError(self, details):
        msg.log('CoinbaseMarketDataFeedHandler - ERROR: {0}'.format(details))
        self.cb.onFeedError(details)

    def onReceived(self, msg):
        pass

    def onOpen(self, msg):
        qtSide = msg['side']
        if 'buy' == qtSide:
            side = MarketSide.BID
        elif 'sell' == qtSide:
            side = MarketSide.ASK
        else:
            self.onError('unexpected side ({0})'.format(msg))
            return None
        quote = Quote(side, Decimal(msg['price']), Decimal(msg['size']), msg['order_id'], msg)
        self.cb.onFeedMsgOpen(quote)

    def onDone(self, msg):
        qtSide = msg['side']
        if 'buy' == qtSide:
            side = MarketSide.BID
        elif 'sell' == qtSide:
            side = MarketSide.ASK
        else:
            self.onError('unexpected side ({0})'.format(msg))
            return None
        quote = Quote(side, Decimal(msg['price']), Decimal(msg['remaining_size']), msg['order_id'], msg)
        self.cb.onFeedMsgDone(quote)

    def onMatch(self, msg):
        # FIXME: format correctly (add 'trade' type)
        self.cb.onFeedMsgMatch(msg)

    def onChange(self, msg):
        # FIXME: format correctly
        self.cb.onFeedMsgChange(msg)

    def processMessage(self, msg):
        """
        Assumes we're not buffering, and the message sequence number has been checked
        """
        msgType = msg['type']
        if   msgType == 'open':
            self.onOpen(msg)
        elif msgType == 'done':
            self.onDone(msg)
        elif msgType == 'match':
            self.onMatch(msg)
        elif msgType == 'received':
            # FIXME: consider using this as primary trigger (would mean moving to top of if chain)
            self.onReceived(msg)
        elif msgType == 'change':
            self.onChange(msg)
        elif msgType == 'error':
            self.onError(msg)
        else:
            self.onError(None)

    def startProcessing(self, fromSeqNum):
        """
        Starts processing all messages with sequence number > seqNum,
        and sets the state to 'PROCESSING'
        """
        self.expSeqNum = fromSeqNum + 1
        self.state     = FeedHandlerState.PROCESSING
        for msg in self.bufferedMessages:
            seqNum = msg['sequence']
            if seqNum > fromSeqNum:
                if seqNum != self.expSeqNum:
                    self.onDataloss()
                    return None
                else:
                    self.expSeqNum += 1
                    self.processMessage(msg)
        self.bufferedMessages = []
        # FIXME: we can add a hook into cb here, if needed...

    def onMessage(self, msg):
        if FeedHandlerState.PROCESSING == self.state:
            seqNum = msg['sequence']
            if seqNum == self.expSeqNum:
                self.expSeqNum += 1
                self.processMessage(msg)
            else:
                self.onDataloss()
        elif FeedHandlerState.BUFFERING == self.state:
            self.bufferedMessages.append(msg)

class CoinbaseWebSocketClient(WebSocketClientProtocol):
    def onConnect(self, response):
        self.log('onConnect - response[{0}]'.format(response))

    def onOpen(self):
        self.log('line open')
        msgData = {'type': 'subscribe', 'product_id': 'BTC-USD'} # FIXME: get product otherwise
        msgJson = json.dumps(msgData)
        self.log('subscribing to book L3 data [{0}]'.format(msgJson))
        self.sendMessage(msgJson)

    def onMessage(self, msg, binary):
        self.log('onMessage - message[{0}]'.format(msg))
        msgDic = json.loads(msg)
        cbc    = self.factory.coinbaseClient
        if ClientState.RUNNING == cbc.clientState:
            self.log('onMessage - RUNNING - processing[{0}]'.format(msg))
        elif ClientState.WAITING_FOR_BOOK_SNAPSHOT == cbc.clientState:
            self.log('onMessage - WAITING_FOR_BOOK_SNAPSHOT - enqueuing[{0}]'.format(msg))
            cbc.wsBuffer.append(msgDic)
        elif ClientState.INITIALIZING_BOOK == cbc.clientState:
            cbc.wsBuffer.append(msgDic)
            self.log('onMessage - INITIALIZING_BOOK - will process {0} buffered messages'.format(len(cbc.wsBuffer)))
            cbc.clientState = ClientState.RUNNING
            self.log('onMessage - switched to RUNNING state')
        elif ClientState.INITIALIZING == cbc.clientState:
            cbc.getBookInitialSnapshot()

    def log(self, msg):
        log.msg('CoinbaseWebSocketClient - {0}'.format(msg))

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
            body.addErrback(cb)
            return body
    
    def _getData(self, req, cb, errorCb):
        agent = Agent(reactor)
        d = agent.request('GET', '{0}/{1}'.format(self.apiUri, req), self._headers(), None)
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
        
def printBody(body):
    print 'Received body:'
    print body

def onError(x):
    print "onError - aborting"
    reactor.stop()

def myFloEmit(self, eventDict):
    text = log.textFromEventDict(eventDict)
    if text is None:
        return None
    self.timeFormat = "%Y%m%d-%H:%M:%S.%f %z"
    timeStr = self.formatTime(eventDict["time"])
    util.untilConcludes(self.write, timeStr + " " + text + "\n")
    util.untilConcludes(self.flush)

class CoinbaseClientService(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def dataReceived(self, data):
        log.msg('CoinbaseClientService - dataReceived[{0}]'.format(data))
        cmdData = json.loads(data)
        self.factory.coinbaseClient.onCommand(cmdData)

class CoinbaseClientServiceFactory(protocol.Factory):
    def __init__(self, coinbaseClient):
        self.coinbaseClient = coinbaseClient

    def buildProtocol(self, addr):
        return CoinbaseClientService(self)

class CoinbaseClient:
    def __init__(self, config):
        prec = config.getint('coinbase', 'decimalPrec')
        self.svcPort     = config.getint('coinbase', 'servicePort')
        self.log('setting service port to {0}'.format(self.svcPort))
        reactor.listenTCP(self.svcPort, CoinbaseClientServiceFactory(self))
        self.log('setting decimal precision to {0}'.format(prec))
        self.clientState = ClientState.INITIALIZING
        decimal.getcontext().prec = prec
        self.restClient  = CoinbaseRestClient(config.get('coinbase', 'clientName'), config.get('coinbase', 'restApiUri'))
        self.product     = config.get('coinbase', 'product')
        self.log('product[{0}]'.format(self.product))
        self.time        = None
        self.qtInc       = "0.01" # expected quote increment
        self.basePrice   = None   # to base the order books off
        self.wsAddress   = config.get('coinbase', 'webSocket')
        self.wsBuffer    = []
        self.log('websocket[{0}]'.format(self.wsAddress))
        reactor.callWhenRunning(self.whenRunning)

    def log(self, msg):
        log.msg('CoinbaseClient - {0}'.format(msg))

    def fatal(self, msg):
        log.msg('CoinbaseClient - FATAL - {0}'.format(msg))
        self.exit()

    def exit(self):
        log.msg('CoinbaseClient - EXITING')
        self.clientState = ClientState.EXITING
        self.stop()

    def whenRunning(self):
        self.log('reactor running')
        # The order is as follows:
        # 1. we get the time (to make sure the server is up)
        # 2. we get the currencies (and check the precision at which we're rounding)
        # 3. we get the products (to make sure the expected product is there, and check parameters)
        # 4. we get the ticker (last trade): the last spot will be used to base the order books off
        # 5. we subscribe to the websocket feed
        # 6. we retrieve a snapshot of the L3 data
        # 7. we initialize the order book from a snapshot, then replay the stored messages from the feed
        self.restClient.getTime(self.onTime, self.onRestClientError)

    def onTime(self, data):
        self.log('onTime: {0}'.format(data))
        self.restClient.getCurrencies(self.onCurrencies, self.onRestClientError)

    def onCurrencies(self, data):
        self.log('onCurrencies: {0}'.format(data))
        ccies = json.loads(data)
        for ccy in ccies:
            if "BTC" == ccy.get("id", None):
                # we check whether the precision we set was enough
                minSize = Decimal(ccy.get("min_size", "0"))
                if Decimal(0) == minSize:
                    self.fatal("insufficient precision")
                self.log("bitcoin size precision checked")
                self.restClient.getProducts(self.onProducts, self.onRestClientError)
                return None
        self.fatal("could not retrieve currency details for BTC")

    def onProducts(self, data):
        self.log('received product list from exchange')
        products = json.loads(data)
        for product in products:
            if product.get("id", None) == self.product:
                self.log("product '{0}' found ({1})".format(self.product, product))
                qtCcy = product.get("quote_currency", None)
                if "USD" != qtCcy:
                    self.fatal("unexpected quote currency (found {0}, expected USD)".format(qtCcy))
                self.log("quote currency checked for {0}".format(self.product))
                qtInc = product.get("quote_increment", None)
                if qtInc != self.qtInc:
                    self.fatal("quote increment check failed for {0} (found {1}, expecting {2})".format(self.product, qtInc, self.qtInc))
                self.log("quote increment checked for {0}".format(self.product))
                self.restClient.getTicker(self.product, self.onTicker, self.onRestClientError)
                return None
        self.fatal("could not find product '{0}'".format(self.product))

    def onBookInitialSnapshot(self, data):
        self.log('received full book snapshot from exchange')
        bookDic = json.loads(data)
        self.log('book snapshot at sequence number {0} ({1} bids, {2} asks)'.format(
            bookDic.get('sequence', None), 
            len(bookDic.get('bids', None)), 
            len(bookDic.get('asks', None))
        ))
        self.clientState = ClientState.INITIALIZING_BOOK
        self.log('onBookInitialSnapshot - switched to INITIALIZING_BOOK state')

    def getBookInitialSnapshot(self):
        if ClientState.INITIALIZING != self.clientState:
            self.fatal('getBookInitialSnapshot called with unexpected state {0}'.format(self.clientState))
        self.log('getBookInitialSnapshot - requesting book L3 snapshot')
        self.restClient.getOrderBook(self.product, 3, self.onBookInitialSnapshot, self.onRestClientError)
        self.clientState = ClientState.WAITING_FOR_BOOK_SNAPSHOT
        self.log('getBookInitialSnapshot - switched to WAITING_FOR_BOOK_SNAPSHOT state')

    def onTicker(self, data):
        """
        Called upon reception of the initial 'ticker' data, triggers WebSocket market data subscription
        """
        self.log('onTicker, data[{0}'.format(data))
        ticker = json.loads(data)
        self.log('received ticker from exchange {0}'.format(data))
        price  = ticker.get("price", None)
        if price is None:
            self.fatal("could not retrieve price")
        self.basePrice = Decimal(price)
        self.log('retrieved base price for {0}: {1}'.format(self.product, self.basePrice))
        self.log('starting websocket connection')
        factory                = WebSocketClientFactory(self.wsAddress)
        factory.protocol       = CoinbaseWebSocketClient
        factory.coinbaseClient = self
        connectWS(factory)

    def onRestClientError(self, x):
        self.fatal('onRestClientError[{0}]'.format(x))

    def onCommand(self, cmdData):
        """
        Callback delivering commands received over TCP
        """
        command = cmdData.get('command', None)
        self.log('received command {0}'.format(command))
        if ServiceCommand.EXIT == command:
            self.exit()
        else:
            self.log('unhandled command')

    def run(self):
        reactor.run()

    def stop(self):
        reactor.stop()

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
