import ConfigParser
from twisted.internet import reactor
from twisted.application.service import Application
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python import log, util
from twisted.python.logfile import DailyLogFile
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
import sys
import json
import decimal
from decimal import Decimal
from enums import MarketSide, OrderSide
from order import Quote, BookSide, Tob

decimal.getcontext().prec = 10

config = None

class ClientProtocol(WebSocketClientProtocol):
    def __init__(self):
        self.lastSequenceNumber = -1
        self.is_closed = False
        priceLB  = Decimal(config.get("coinbase", "priceLowerBound"))
        priceUB  = Decimal(config.get("coinbase", "priceUpperBound"))
        priceRes = Decimal(config.get("coinbase", "priceResolution"))
        self.bookSides = dict()
        self.bookSides[ MarketSide.BID ] = BookSide(MarketSide.BID, priceRes, priceLB, priceUB)
        self.bookSides[ MarketSide.ASK ] = BookSide(MarketSide.ASK, priceRes, priceLB, priceUB)
        self.tob       = dict()
        self.tob[ MarketSide.BID ] = None
        self.tob[ MarketSide.ASK ] = None
        self.orders    = dict()

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def initMessage(self):
        message_data = {"type": "subscribe", "product_id": "BTC-USD"}
        message_json = json.dumps(message_data)
        print "sendMessage: " + message_json
        self.sendMessage(message_json)
        
    def onOpen(self):
        print "onOpen calls initMessage()"
        self.initMessage()

    def onMessage(self, msg, binary):
        msgData = json.loads(msg)
        seqNum  = msgData[ "sequence" ]
        if -1 == self.lastSequenceNumber or seqNum == self.lastSequenceNumber + 1:
            self.lastSequenceNumber = seqNum
        else:
            abort( "Unexpected sequence number received [{0} vs {1}]".format(seqNum, self.lastSequenceNumber) )
        msg_type = msgData[ "type" ]
        if "open" == msg_type:
            self.onOpenMessage(msgData)
        elif "done" == msg_type:
            self.onDoneMessage(msgData)
        elif "match" == msg_type:
            self.onMatchMessage(msgData)
        elif "change" == msg_type:
            self.onChangeMessage(msgData)
        elif "error" == msg_type:
            self.onErrorMessage(msgData)
        elif "received" == msg_type:
            self.onReceivedMessage(msgData)
        else:
            self.onUnexpectedMessage(msgData)

    class UnexpectedMessage(Exception):
        def __init__(self, msg): self.msg = msg

        def __str__(self): return "ClientProtocol::UnexpectedMessage[{0}]".format(self.msg)

    def updateTob(self):
        newTob = (self.bookSides[MarketSide.BID].tobPrice(), self.bookSides[MarketSide.ASK].tobPrice())
        if newTob != self.tob:
            self.tob = newTob
            tobStr = "TOB[{0} - {1}]".format(self.tob[0], self.tob[1])
            print tobStr
            log.msg(tobStr)

    def msgSide(self, msg):
        if "buy" == msg[ "side" ]:
            return MarketSide.BID
        elif "sell" == msg[ "side" ]:
            return MarketSide.ASK
        else:
            raise UnexpectedMessage(msg)

    def onOpenMessage(self, msg):
        side = self.msgSide(msg)
        size = msg.get( "size", msg.get( "remaining_size", None ) )
        if None == size:
            raise UnexpectedMessage(msg)
        size = Decimal(size)
        quote = Quote(side, Decimal(msg["price"]), size, msg["order_id"], msg)
        bs = self.bookSides[side]
        bs.addNewQuote(quote)
        newTob = bs.tob()
        if newTob is None or self.tob[side] is None or newTob != self.tob[side]:
            self.tob[side] = newTob
            log.msg("TOB_UPDATE[{0} - {1} - {2}]".format(msg["time"], side, newTob))

    def onDoneMessage(self, msg):
        side = self.msgSide(msg)
        bs = self.bookSides[side]
        bs.removeQuote(msg["order_id"])
        self.orders.pop(msg["order_id"], None)
        newTob = bs.tob()
        if newTob is None or self.tob[side] is None or newTob != self.tob[side]:
            self.tob[side] = newTob
            log.msg("TOB_UPDATE[{0} - {1} - {2}]".format(msg["time"], side, newTob))

    def onMatchMessage(self, msg):
        side = self.msgSide(msg)
        #print "MATCH[{0}]: {1}".format(side, msg)
        #print "TAKER: {0}".format(self.orders.get(msg["taker_order_id"], None))
        log.msg("TRD_UPDATE[{0} - {1} - {2}x{3}]".format(msg["time"], side, msg["size"], msg["price"]))

    def onChangeMessage(self, msg):
        return 

    def onErrorMessage(self, msg):
        raise UnexpectedMessage(msg)

    def onReceivedMessage(self, msg):
        self.orders[msg["order_id"]] = msg
        return

    def onUnexpectedMessage(self, msg):
        raise UnexpectedMessage(msg)

    def abort( self, msg ):
        print "Aborting (%s)" % msg
        reactor.stop()

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

def myFloEmit(self, eventDict):
    text = log.textFromEventDict(eventDict)
    if text is None:
        return
    self.timeFormat = "%Y%m%d-%H:%M:%S.%f %z"
    timeStr = self.formatTime(eventDict["time"])
    util.untilConcludes(self.write, timeStr + " " + text + "\n")
    util.untilConcludes(self.flush)

if __name__ == '__main__':
    if 2 != len(sys.argv):
        print "Expected unique argument (configuration file)"
    else:
        configFile = sys.argv[1]
        print "Using configuration file '{0}'".format(configFile)
        config = ConfigParser.RawConfigParser()
        config.read(configFile)
        loggingFile = config.get("coinbase", "logfile")
        #loggingDir  = config.get("coinbase", "logdir")

        #application = Application("CoinbaseFeed")
        #application.setComponent(ILogObserver, flo.emit)
        log.FileLogObserver.emit = myFloEmit
        log.startLogging(open(loggingFile, "w"))

        log.msg("coinbase - configuration file '{0}'".format(configFile))
        wsAddress = config.get("coinbase", "websocket")
        print "Connecting to websocket '{0}'".format(wsAddress)
        factory = WebSocketClientFactory(wsAddress)
        factory.protocol = ClientProtocol
        connectWS(factory)
        reactor.run()
