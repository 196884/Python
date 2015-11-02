from twisted.internet import protocol, reactor
import json
from enums import ServiceCommand

class CoinbaseClientCommanderProtocol(protocol.Protocol):
    def connectionMade(self):
        print '{0} - connectionMade'.format(type(self).__name__)
        command = {
            'command': ServiceCommand.EXIT
        }
        cmdJson = json.dumps(command)
        self.transport.write(cmdJson)

    def dataReceived(self, data):
        print '{0} - dataReceived[{1}]'.format(type(self).__name__)

    def connectionLost(self, reason):
        print '{0} - connectionLost, reason[{1}]'.format(type(self).__name__, reason)

class CoinbaseClientCommanderFactory(protocol.ClientFactory):
    #def buildPrococol(self, addr):
        #print '{0} - buildProtocol[{1}]'.format(addr)
        #return CoinbaseClientCommanderProtocol()

    def startedConnecting(self, connector):
        print '{0} - startedConnecting'.format(type(self).__name__)

    def clientConnectionFailed(self, connector, reason):
        print '{0} - clientConnectionFailed[{1}]'.format(type(self).__name__, reason)

    def clientConnectionLost(self, connector, reason):
        print '{0} - clientConnectionLost'.format(type(self).__name__)
        self.exit()

    def exit(self):
        reactor.stop()

def start():
    host = "localhost"
    port = 3414
    factory = CoinbaseClientCommanderFactory()
    factory.protocol = CoinbaseClientCommanderProtocol
    reactor.connectTCP(host, port, factory)
    reactor.run()

if '__main__' == __name__:
    start()
