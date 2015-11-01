from enums import MarketSide
import decimal
from decimal import Decimal

decimal.getcontext().prec = 10
decplaces = Decimal(10) ** -decimal.getcontext().prec

class Quote:
    def __init__(self, side, price, qty, quoteId, rawData = None):
        self.side     = side
        self.price    = price
        self.quantity = qty
        self.quoteId  = quoteId
        self.rawData  = rawData

    def __str__( self ):
        return "[{0}:{1}x{2}]".format( self.side, self.quantity, self.price )

class Tob:
    def __init__(self, price, size):
        self.price = price
        self.size  = size

    def __eq__(self, other):
        return self.price == other.price and self.size == other.size

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "{0}x{1}".format(self.size, self.price)

class PriceLevel:
    def __init__(self, side, price, index):
        self.side       = side
        self.price      = price
        self.index      = index # the index in the book
        self.quantity   = 0
        self.quotesById = dict()

    def __str__(self):
        return "PriceLevel[{0}:{1}x{2}]".format( self.side, self.quantity, self.price )

    def empty(self):
        return len(self.quotesById) == 0

    class WrongPrice(Exception): pass

    def addNewQuote(self, quote):
        if self.price != quote.price:
            raise WrongPrice()
        self.quotesById[ quote.quoteId ] = quote
        self.quantity += quote.quantity

    def removeQuote(self, quoteId):
        oldQuote = self.quotesById.pop(quoteId, None)
        if None == oldQuote:
            return
        self.quantity -= oldQuote.quantity

class BookSide:
    def __init__(self, side, priceResolution, priceLowerBound, priceUpperBound):
        # We store the levels in a list, so we need to convert prices to indices...
        self.side     = side
        self.priceRes = Decimal(priceResolution)
        self.priceLB  = Decimal(priceLowerBound)
        self.priceUB  = Decimal(priceUpperBound)
        price         = Decimal(priceLowerBound)
        self.levels   = []
        self.idToIdx  = dict()
        while price <= priceUpperBound:
            self.levels.append(None)
            price += self.priceRes
        self.tobIdx   = -1

    def indexToPrice(self, index):
        return Decimal(self.priceLB + index * self.priceRes)

    class UnexpectedPrice(Exception):
        def __init__(self, price): self.price = price

        def __str__(self): return "BookSide::UnexpectedPrice[{0}]".format(self.price)

    def priceToIndex(self, price):
        if price < self.priceLB or price > self.priceUB:
            return None # TODO: add support for out of range prices
        idx = int(( price - self.priceLB + Decimal(0.5) * self.priceRes ) // self.priceRes)
        if self.indexToPrice(idx) != price:
            print price
            print self.indexToPrice(idx)
            raise self.UnexpectedPrice(price)
        return idx

    def priceLevel(self, price, create = True):
        idx    = self.priceToIndex(price)
        result = self.levels[idx]
        if result == None and create:
            result           = PriceLevel(self.side, price, idx)
            self.levels[idx] = result
        return result

    def addNewQuote(self, quote):
        if quote.price < self.priceLB or quote.price > self.priceUB:
            return # TODO: add support
        priceLevel = self.priceLevel(quote.price)
        priceLevel.addNewQuote(quote)
        self.idToIdx[ quote.quoteId ] = priceLevel.index
        if self.tobIdx < 0:
            self.tobIdx = priceLevel.index
        else:
            if MarketSide.BID == self.side:
                self.tobIdx = max(self.tobIdx, priceLevel.index)
            else:
                self.tobIdx = min(self.tobIdx, priceLevel.index)

    def updateTobIndex(self):
        if MarketSide.BID == self.side:
            while self.tobIdx >= 0 and None == self.levels[self.tobIdx]:
                self.tobIdx -= 1
        else:
            maxIdx = len(self.levels)
            while self.tobIdx < maxIdx and None == self.levels[self.tobIdx]:
                self.tobIdx += 1
            if self.tobIdx >= maxIdx:
                self.tobIdx = -1

    def removeQuote(self, quoteId):
        idx = self.idToIdx.pop(quoteId, None)
        if None == idx:
            return
        priceLevel = self.levels[idx]
        if None == priceLevel:
            return # TODO: add logging
        priceLevel.removeQuote(quoteId)
        if priceLevel.empty():
            self.levels[idx] = None
            self.updateTobIndex()

    def tob(self):
        if self.tobIdx < 0:
            return None
        tobLevel = self.levels[self.tobIdx]
        return Tob(tobLevel.price, tobLevel.quantity)
