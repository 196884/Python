import sys
import json
import ConfigParser
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
from decimal import Decimal
from enums import defEnum
from order_book import MarketSide, Quote
from file_log_observer import CoinbaseFileLogObserver

FeedHandlerState = defEnum('INACTIVE', 'BUFFERING', 'PROCESSING', 'DATALOSS')

class IMarketDataFeedHandlerCB:
    def onFeedActive(self, seqNum):
        """
        Called when the first message comes in and gets buffered
        """
        pass

    def onFeedDataloss(self):
        pass

    def onFeedError(self, error):
        pass

    def onFeedMsgOpen(self, quote):
        pass

    def onFeedMsgDoneLimit(self, quote):
        pass

    def onFeedMsgDoneMarket(self, msg):
        pass

    def onFeedMsgMatch(self, match):
        pass

    def onFeedMsgChange(self, change):
        pass

class UnexpectedMessageFormat(Exception):
    def __init__(self, msg):
        self.msg = msg

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
        self.active           = False

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
        size = msg.get('size', msg.get('remaining_size', None))
        if size is None:
            raise UnexpectedMessageFormat(msg)
        quote = Quote(side, Decimal(msg['price']), Decimal(size), msg['order_id'], msg)
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
        orderType = msg['order_type']
        if   'market' == orderType:
            self.cb.onFeedMsgDoneMarket(msg)
        elif 'limit'  == orderType:
            quote = Quote(side, Decimal(msg['price']), Decimal(msg['remaining_size']), msg['order_id'], msg)
            self.cb.onFeedMsgDoneLimit(quote)
        else:
            raise UnexpectedMessageFormat(msg)

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
                return
            else:
                self.onDataloss()
                return
        elif FeedHandlerState.BUFFERING == self.state:
            self.bufferedMessages.append(msg)
            if not self.active:
                log.msg('CoinbaseMarketDataFeedHandler - active')
                self.cb.onFeedActive(msg.get('sequence', None))
                self.active = True
            return
        # FIXME: remove logging
        log.msg('buffer size: {0}'.format(len(self.bufferedMessages)))
        

class CoinbaseWebSocketClient(WebSocketClientProtocol):
    def onConnect(self, response):
        self.log('onConnect - response[{0}]'.format(response))

    def onOpen(self):
        self.log('line open')
        msgData = {'type': 'subscribe', 'product_id': self.factory.product}
        msgJson = json.dumps(msgData)
        self.log('subscribing to book L3 data [{0}]'.format(msgJson))
        self.sendMessage(msgJson)

    def onMessage(self, msg, binary):
        self.log('onMessage - message[{0}]'.format(msg))
        msgDic = json.loads(msg)
        self.factory.feedHandler.onMessage(msgDic)
       
    def log(self, msg):
        log.msg('CoinbaseWebSocketClient - {0}'.format(msg))

class NoFeedHandlerSet(Exception): pass

class CoinbasePriceFeed:
    def __init__(self, config):
        self.wsAddress      = config.get('coinbase', 'webSocket')
        self.product        = config.get('coinbase', 'product')
        factory             = WebSocketClientFactory(self.wsAddress)
        factory.protocol    = CoinbaseWebSocketClient
        factory.product     = self.product
        factory.feedHandler = None
        self.factory        = factory

    def createFeedHandler(self, cb):
        self.factory.feedHandler = CoinbaseMarketDataFeedHandler(cb)
        return self.factory.feedHandler

    def connect(self):
        if self.factory.feedHandler is None:
            raise NoFeedHandlerSet()
        log.msg('CoinbasePriceFeed - connect')
        connectWS(self.factory)

############################################
# For testing

class TestAlgo(IMarketDataFeedHandlerCB):
    def __init__(self, config):
        self.log('initializing')
        self.config           = config
        self.priceFeed        = CoinbasePriceFeed(config)
        self.mdFeedHandler    = self.priceFeed.createFeedHandler(self)
        self.mdFeedHandler.startBuffering()

    def startPriceFeed(self):
        """
        Puts the feed handler in buffering state, and connects the price feed
        """
        # TODO: check current pf state
        self.mdFeedHandler.startBuffering()
        self.priceFeed.connect()

    ### IMarketDataFeedHandlerCB - BEGIN ###
    def onFeedActive(self, seqNum):
        self.log('onFeedActive - sequence[{0}]'.format(seqNum))
        self.mdFeedHandler.startProcessing(seqNum)

    def onFeedDataloss(self):
        self.log('onFeedDataloss')

    def onFeedError(self, error):
        self.log('onFeedError')

    def onFeedMsgOpen(self, quote):
        self.log('onFeedMsgOpen')
        #self.orderBookBuilder.addQuote(quote)

    def onFeedMsgDoneLimit(self, quote):
        self.log('onFeedMsgDoneLimit')
        #self.orderBookBuilder.removeQuote(quote)

    def onFeedMsgDoneMarket(self, msg):
        self.log('onFeedMsgDoneMarket')

    def onFeedMsgMatch(self, match):
        self.log('onFeedMsgMatch')

    def onFeedMsgChange(self, change):
        self.log('onFeedMsgChange')
    ### IMarketDataFeedHandlerCB -  END  ###

    def startProcessing(self, seqNum):
        self.log('startProcessing')
        self.mdFeedHandler.startProcessing(seqNum)

    def log(self, msg):
        log.msg('Algo - {0}'.format(msg))


if '__main__' == __name__:
    if 2 != len(sys.argv):
        print "Expected unique argument (configuration file)"
    else:
        configFile = sys.argv[1]
        config = ConfigParser.RawConfigParser()
        config.read(configFile)
        loggingFile = config.get("coinbase", "logFile")
        print "logging to '{0}'".format(loggingFile)
        log.FileLogObserver = CoinbaseFileLogObserver
        log.startLogging(open(loggingFile, 'w'))
        algo = TestAlgo(config)
        reactor.callWhenRunning(lambda: algo.startPriceFeed())
        reactor.run()
