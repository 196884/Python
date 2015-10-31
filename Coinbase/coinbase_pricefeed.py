from twisted.internet import reactor
from twisted.python import log
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
import json
import decimal
from decimal import Decimal
from enums import MarketSide, OrderSide
from order import Quote, BookSide

decimal.getcontext().prec = 10

loggingFile = "/Users/regisdupont/Documents/Code/Python/Coinbase/log.txt"

class ClientProtocol(WebSocketClientProtocol):
    def __init__(self):
        self.lastSequenceNumber = -1
        self.is_closed = False
        self.bookSides = dict()
        self.bookSides[ MarketSide.BID ] = BookSide(MarketSide.BID, 0.01, 280, 380)
        self.bookSides[ MarketSide.ASK ] = BookSide(MarketSide.ASK, 0.01, 280, 380)
        self.tob       = (None, None)
        self.orders    = dict()
        log.startLogging(open(loggingFile, 'w'))

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
        self.bookSides[side].addNewQuote(quote)
        self.updateTob()

    def onDoneMessage(self, msg):
        side = self.msgSide(msg)
        self.bookSides[side].removeQuote(msg["order_id"])
        self.orders.pop(msg["order_id"], None)
        self.updateTob()

    def onMatchMessage(self, msg):
        print "MATCH[{0}]: {1}".format(self.msgSide(msg), msg)
        print "TAKER: {0}".format(self.orders.get(msg["taker_order_id"], None))
        return 

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

if __name__ == '__main__':
    factory = WebSocketClientFactory("wss://ws-feed.exchange.coinbase.com")
    factory.protocol = ClientProtocol
    connectWS(factory)
    reactor.run()
