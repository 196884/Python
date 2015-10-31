from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
import json
import decimal
from decimal import Decimal
from enums import MarketSide, OrderSide
from order import Quote, BookSide

decimal.getcontext().prec = 10

class ClientProtocol(WebSocketClientProtocol):
    def __init__(self):
        self.lastSequenceNumber = -1
        self.is_closed = False
        self.bookSides = dict()
        self.bookSides[ MarketSide.BID ] = BookSide(MarketSide.BID, 0.01, 280, 380)
        self.bookSides[ MarketSide.ASK ] = BookSide(MarketSide.ASK, 0.01, 280, 380)

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
        print "********************************"
        print "Got echo: " + msg
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
        return 
        msg_side = msgData[ "side" ]
        if "buy" == msg_side:
            side = OrderSide.BUY
        elif "sell" == msg_side:
            side = OrderSide.SELL
        else:
            side = None # FIXME: throw!
        msg_type = msgData[ "type" ]
        if msg_type == "done":
            msg_reason = msgData[ "reason" ]
            if msg_reason != "canceled":
                print "###############################################"
                print self.lastSequenceNumber 
                print "###############################################"
                self.abort( "saw what we were looking for" )
        if "received" == msg_type:
            quote = Quote( side, msgData[ "price" ], msgData[ "size" ] )
            print quote

    class UnexpectedMessage(Exception):
        def __init__(self, msg): self.msg = msg

        def __str__(self): return "ClientProtocol::UnexpectedMessage[{0}]".format(self.msg)

    def printTobPrices(self):
        print "TobPrices: {0} - {1}".format(self.bookSides[MarketSide.BID].tobPrice(), self.bookSides[MarketSide.ASK].tobPrice())

    def onOpenMessage(self, msg):
        if "buy" == msg[ "side" ]:
            side = MarketSide.BID
        elif "sell" == msg[ "side" ]:
            side = MarketSide.ASK
        else:
            raise UnexpectedMessage(msg)
        size = msg.get( "size", msg.get( "remaining_size", None ) )
        if None == size:
            raise UnexpectedMessage(msg)
        size = Decimal(size)
        quote = Quote(side, Decimal(msg["price"]), size, msg)
        self.bookSides[side].addNewQuote(quote)
        print quote
        self.printTobPrices()

    def onDoneMessage(self, msg):
        if "buy" == msg[ "side" ]:
            side = MarketSide.BID
        elif "sell" == msg[ "side" ]:
            side = MarketSide.ASK
        else:
            raise self.UnexpectedMessage(msg)
        self.bookSides[side].removeQuote(msg["order_id"])
        self.printTobPrices()

    def onMatchMessage(self, msg):
        return 

    def onChangeMessage(self, msg):
        return 

    def onErrorMessage(self, msg):
        raise UnexpectedMessage(msg)

    def onReceivedMessage(self, msg):
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
