from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
import json

class ClientProtocol(WebSocketClientProtocol):
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
        print "Got echo: " + msg

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

if __name__ == '__main__':
    factory = WebSocketClientFactory("wss://ws-feed.exchange.coinbase.com")
    factory.protocol = ClientProtocol
    connectWS(factory)
    reactor.run()
