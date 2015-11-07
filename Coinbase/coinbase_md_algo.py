import sys
import json
import ConfigParser
from twisted.python import log
from twisted.internet import reactor
import decimal
from decimal import Decimal
from enums import defEnum
from order_book import MarketSide, Quote, OrderBookBuilder
from file_log_observer import CoinbaseFileLogObserver
from exchange_price_feed import IMarketDataFeedHandlerCB, CoinbasePriceFeed
from exchange_request_response_api import CoinbaseRequestResponseAPI

class UnknownOrderType(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'UnknownOrderType[{0}]'.format(msg)

class CoinbaseMDAlgo(IMarketDataFeedHandlerCB):
    def __init__(self, config):
        self.log('initializing')
        self.config           = config
        self.product          = config.get('coinbase', 'product')
        prec                  = config.getint('coinbase', 'decimalPrec')
        self.log('setting decimal precision to {0}'.format(prec))
        decimal.getcontext().prec = prec
        self.maxMove          = Decimal(config.get('coinbase', 'maxMove'))
        self.reqRespAPI       = CoinbaseRequestResponseAPI(config)
        self.priceFeed        = CoinbasePriceFeed(config)
        self.mdFeedHandler    = self.priceFeed.createFeedHandler(self)
        self.mdFeedHandler.startBuffering()
        self.orderBookBuilder = None
        self.takerOrders      = dict()

    def startPriceFeed(self):
        """
        Puts the feed handler in buffering state, and connects the price feed
        """
        # TODO: check current pf state
        self.log('connecting price feed')
        self.mdFeedHandler.startBuffering()
        self.priceFeed.connect()
        # At this point, we wait for a callback into 'onFeedActive'
        # TODO: timeout?

    ### IMarketDataFeedHandlerCB - BEGIN ###
    def onFeedActive(self, seqNum):
        self.log('onFeedActive - sequence[{0}]'.format(seqNum))
        self.log('requesting full order book snapshot for {0}'.format(self.product))
        self.reqRespAPI.getOrderBook(self.product, 3, self.onBookSnapshot, self.onRequestError)
        #self.mdFeedHandler.startProcessing(seqNum)

    def onFeedDataloss(self):
        self.log('onFeedDataloss')

    def onFeedError(self, error):
        self.log('onFeedError')

    def onFeedMsgReceived(self, msg):
        orderType = msg['order_type']
        if   orderType == 'market':
            self.log('onFeedMsgReceived - MARKET ORDER [{0}]'.format(msg))
        elif orderType == 'limit':
            return
        else:
            raise UnknownOrderType(msg)

    def onFeedMsgOpen(self, quote):
        self.log('onFeedMsgOpen       - {0}'.format(quote))
        if self.orderBookBuilder.addQuote(quote):
            self.log('new TOB: {0} vs {1}'.format(self.orderBookBuilder.topOfBook(MarketSide.BID), self.orderBookBuilder.topOfBook(MarketSide.ASK)))
        #self.orderBookBuilder.addQuote(quote)

    def onFeedMsgDoneLimit(self, quote):
        self.log('onFeedMsgDoneLimit  - {0}'.format(quote))
        taker = self.takerOrders.pop(quote.orderId, None)
        if taker is None:
            if self.orderBookBuilder.removeQuote(quote):
                self.log('new TOB: {0} vs {1}'.format(self.orderBookBuilder.topOfBook(MarketSide.BID), self.orderBookBuilder.topOfBook(MarketSide.ASK)))
        else:
           self.log('onFeedMsgDoneLimit - {0} oustanding taker orders'.format(len(self.takerOrders)))

    def onFeedMsgDoneMarket(self, msg):
        self.log('onFeedMsgDoneMarket - {0}'.format(msg))

    def onFeedMsgMatch(self, match):
        takerOrderId = match['taker_order_id']
        self.takerOrders[takerOrderId] = match
        if match['side'] == 'sell':
            side = MarketSide.ASK
        else:
            side = MarketSide.BID
        self.log('MATCH - {0}'.format(match))
        self.orderBookBuilder.applyFill(side, match['maker_order_id'], Decimal(match['size']))
        self.log('new TOB: {0} vs {1}'.format(self.orderBookBuilder.topOfBook(MarketSide.BID), self.orderBookBuilder.topOfBook(MarketSide.ASK)))
        self.log('onFeedMsgMatch - {0} outstanding taker orders'.format(len(self.takerOrders)))

    def onFeedMsgChange(self, change):
        self.log('onFeedMsgChange - {0}'.format(change))
    ### IMarketDataFeedHandlerCB -  END  ###

    ### Callbacks for the request/response API - BEGIN ###
    def onTime(self, timeData):
        self.log('timestamp received from exchange - {0}'.format(timeData['iso']))
        self.reqRespAPI.getCurrency('BTC', self.onBTC, self.onRequestError)

    def onBTC(self, ccyData):
        self.log('bitcoin currency data received from exchange - {0}'.format(ccyData))
        if Decimal(ccyData['min_size']) == Decimal(0):
            self.fatal('precision too low')
        self.reqRespAPI.getProduct(self.product, self.onProduct, self.onRequestError)

    def onProduct(self, prodData):
        self.log('{0} product data received from exchange - {1}'.format(self.product, prodData))
        if prodData['id'] != self.product:
            self.fatal('unexpected product name received from exchange - {0}'.format(prodData))
        if prodData['quote_increment'] != '0.01':
            self.fatal('unexpected quote increment - {0}'.format(prodData))
        if prodData['base_min_size'] != '0.01':
            self.fatal('unexpected base min size - {0}'.format(prodData))
        # At this point, all the checks should be done: we are ready to get the market data
        self.startPriceFeed()

    def onBookSnapshot(self, product, level, book, sequence):
        if product != self.product or level != 3:
            self.fatal('unexpected product / level snapshot received')
        self.log('received initial book snapshot')
        priceInc = Decimal('0.01')
        basePrice = max([ q.price for q in book[ MarketSide.BID ] ])
        self.log('setting base price to {0}'.format(basePrice))
        self.log('initializing order book builder')
        self.orderBookBuilder = OrderBookBuilder(priceInc, basePrice, self.maxMove, book)
        self.log('order book builder initialized')
        self.log('initial TOB: {0} vs {1}'.format(self.orderBookBuilder.topOfBook(MarketSide.BID), self.orderBookBuilder.topOfBook(MarketSide.ASK)))
        self.mdFeedHandler.startProcessing(sequence)

    def onRequestError(self, data):
        self.fatal( 'request-response API error: {0}'.format(data))

    ### Callbacks for the request/response API -  END  ###

    def start(self):
        """
        Main entry point - to call when the reactor is running
        """
        self.reqRespAPI.getTime(self.onTime, self.onRequestError)
        #self.startPriceFeed()

    def log(self, msg):
        log.msg('CoinbaseMDAlgo - {0}'.format(msg))

    def fatal(self, msg):
        log.msg('CoinbaseMDAlgo - FATAL - {0}'.format(msg))
        reactor.stop()

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
        algo = CoinbaseMDAlgo(config)
        reactor.callWhenRunning(lambda: algo.start())
        reactor.run()
