import decimal
from decimal import Decimal
from enums import defEnum

MarketSide  = defEnum( 'BID', 'ASK' )

class UnexpectedQuote(Exception):
    def __init__(self, quote):
        self.quote = quote

    def __str__(self):
        return 'UnexpectedQuote[{0}]'.format(self.quote)

class QuoteNotFound(Exception):
    def __init__(self, orderId):
        self.orderId = orderId

    def __str__(self):
        return 'QuoteNotFound[{0}]'.format(self.orderId)

class InconsistentQuoteSize(Exception):
    def __init__(self, received, inBook):
        self.received = received
        self.inBook   = inBook

    def __str__(self):
        return 'InconsistentQuoteSize: received[{0}] vs in book[{1}]'.format(self.received, self.inBook)

class Quote:
    """
    Representing a single quote
    """
    def __init__(self, side, price, size, orderId, rawData = None):
        self.side    = side
        self.price   = price
        self.size    = size
        self.orderId = orderId
        self.rawData = rawData

    def __str__(self):
        return 'Quote[{0}: {1} x {2} - {3}]'.format(self.side, self.price, self.size, self.orderId)

class BookPriceLevelAggregate:
    """
    Representing the aggregate of all quotes at a given price level.
    """
    def __init__(self, price, quantity, nbQuotes):
        self.price    = price
        self.quantity = quantity
        self.nbQuotes = nbQuotes

    def __str__(self):
        return 'BookPriceLevelAggregate[ {0} x {1} : {2} quote(s) ]'.format(self.price, self.quantity, self.nbQuotes )

class BookPriceLevel:
    """
    Representing a single price level.
    """
    def __init__(self, price, index):
        self.price    = price
        self.index    = index
        self.quantity = 0
        self.quotes   = dict()

    def __str__(self):
        #return 'BookPriceLevel[ {0} x {1} : {2} quotes ]'.format(self.price, self.quantity, len(self.quotes))
        return 'BookPriceLevel[ {0} x {1} : {2} quotes {3} ]'.format(self.price, self.quantity, len(self.quotes), self.quotes.keys())

    def empty(self):
        return len(self.quotes) == 0

    def addQuote(self, quote):
        if quote.price != self.price or quote.orderId in self.quotes.keys() or quote.size <= 0:
            raise UnexpectedQuote(quote)
        self.quotes[quote.orderId] = quote
        self.quantity += quote.size

    def removeQuote(self, quote):
        """
        Returns True iff the level is now empty
        """
        bookQuote = self.quotes.pop(quote.orderId, None)
        if bookQuote is None:
            raise QuoteNotFound(quote)
        if 0 == len(self.quotes):
            self.quantity = Decimal(0)
            return True
        else:
            self.quantity = sum([ q.size for q in self.quotes.values() ])
            return False

    def applyFill(self, orderId, filledQty):
        self.quotes[orderId].size -= filledQty
        self.quantity             -= filledQty
        # Note that it's possible to end up with a quantity of zero,
        # which should be followed by a 'removeQuote'

class InvalidPrice(Exception):
    def __init__(self, price):
        self.price = price

    def __str__(self):
        return 'InvalidPrice[{0}]'.format(self.price)

class QuoteOutOfBook(Exception):
    def __init__(self, quote):
        self.quote = quote

    def __str__(self):
        return 'QuoteOutOfBook[{0}]'.format(self.quote)

class EmptyBook(Exception): pass

    
class OrderBookSide:
    """
    Stores a given side of the order book
    """
    def __init__(self, side, priceInc, minPrice, maxPrice, snapshot = []):
        self.side       = side
        self.priceInc   = priceInc
        self.priceLB    = (minPrice // priceInc) * priceInc
        self.priceUB    = (maxPrice // priceInc) * priceInc
        self.levels     = []
        priceCurr       = self.priceLB
        while priceCurr <= self.priceUB:
            self.levels.append(None)
            priceCurr  += self.priceInc
        self.maxIdx     = len(self.levels) - 1
        self.initFromSnapshot(snapshot)

    def topOfBook(self):
        return self.levels[self.tobIdx]

    def _priceToIndex(self, price):
        if price < self.priceLB or price > self.priceUB:
            return None
        index = (price - self.priceLB) // self.priceInc
        # FIXME: remove safety check?
        if price != self.priceLB + index * self.priceInc:
            print('Expected {0} ({1}, {2}, {3})'.format(self.priceLB + index * self.priceInc, self.priceLB, index, self.priceInc))
            raise InvalidPrice(price)
        return int(index)

    def getPriceLevel(self, price, create = True):
        """
        Retrieves the PriceLevel for a given price, creating it if needed.

        Returns None if the price is out of book range
        """
        index = self._priceToIndex(price)
        if index is None:
            return None
        result = self.levels[index]
        if result is None and create:
            result = BookPriceLevel(price, index)
            self.levels[index] = result
        return result

    def addQuote(self, quote):
        """
        Returns True iff the tob has moved
        """
        priceLevel = self.getPriceLevel(quote.price)
        if priceLevel is None:
            if MarketSide.BID == self.side:
                if quote.price > self.priceUB:
                    raise QuoteOutOfBook(quote)
            else:
                if quote.price < self.priceLB:
                    raise QuoteOutOfBook(quote)
            self.oobQuotes[quote.orderId] = quote
            return False
        else:
            priceLevel.addQuote(quote)
            if MarketSide.BID == self.side:
                if priceLevel.index >=self.tobIdx:
                    self.tobIdx = priceLevel.index
                    return True
                else:
                    return False
            else:
                if priceLevel.index <=self.tobIdx:
                    self.tobIdx = priceLevel.index
                    return True
                else:
                    return False

    def _updateTob(self, index):
        if MarketSide.BID == self.side:
            while index >= 0 and self.levels[index] is None:
                index -= 1
            if index < 0:
                raise EmptyBook()
            self.tobIdx = index
        else:
            while index <= self.maxIdx and self.levels[index] is None:
                index += 1
            if index > self.maxIdx:
                raise EmptyBook()
            self.tobIdx = index

    def removeQuote(self, quote):
        """
        Returns True iff the tob has moved
        """
        priceLevel = self.getPriceLevel(quote.price, False)
        if priceLevel is None:
            if self.oobQuotes.pop(quote.orderId, None) is None:
                raise QuoteNotFound(quote)
            return False
        else:
            index = priceLevel.index
            if priceLevel.removeQuote(quote):
                self.levels[index] = None
                if index == self.tobIdx:
                    self._updateTob(index)
                    return True
                else:
                    return False
            else:
                return index == self.tobIdx

    def applyFill(self, orderId, quantityFilled):
        priceLevel = self.levels[self.tobIdx]
        priceLevel.applyFill(orderId, quantityFilled)

    def clear(self):
        nbLevels       = len(self.levels)
        self.levels    = [ None for i in range(nbLevels) ]
        if MarketSide.BID == self.side:
            self.tobIdx = 0
        else:
            self.tobIdx = self.maxIdx
        self.oobQuotes = dict()

    def initFromSnapshot(self, snapshot):
        self.clear()
        for quote in snapshot:
            self.addQuote(quote)

class OrderBookBuilder:
    def __init__(self, priceInc, basePrice, maxMove, snapshot = dict()):
        self.orderBookSides = {
            MarketSide.BID: OrderBookSide(MarketSide.BID, priceInc, basePrice - maxMove, basePrice + maxMove),
            MarketSide.ASK: OrderBookSide(MarketSide.ASK, priceInc, basePrice - maxMove, basePrice + maxMove),
        }
        self.initFromSnapshot(snapshot)

    def initFromSnapshot(self, snapshot):
        bids = snapshot.get(MarketSide.BID, [])
        asks = snapshot.get(MarketSide.ASK, [])
        print 'OrderBookBuilder - initFromSnapshot ({0} bids, {1} asks)'.format(len(bids), len(asks))
        self.orderBookSides[MarketSide.BID].initFromSnapshot(bids)
        self.orderBookSides[MarketSide.ASK].initFromSnapshot(asks)

    def addQuote(self, quote):
        return self.orderBookSides[quote.side].addQuote(quote)

    def removeQuote(self, quote):
        return self.orderBookSides[quote.side].removeQuote(quote)

    def applyFill(self, side, orderId, quantityFilled):
        self.orderBookSides[side].applyFill(orderId, quantityFilled)

    def topOfBook(self, side):
        return self.orderBookSides[side].topOfBook()

def test1():
    bidBook = OrderBookSide(MarketSide.BID, Decimal("0.01"), Decimal("99"), Decimal("101"))
    bidBook.initFromSnapshot([
        Quote(MarketSide.BID, Decimal(" 20.00"), Decimal("1"), "001"),
        Quote(MarketSide.BID, Decimal("100.01"), Decimal("2"), "002"),
        Quote(MarketSide.BID, Decimal("100.05"), Decimal("7"), "003"),
        Quote(MarketSide.BID, Decimal("100.02"), Decimal("2"), "004"),
        Quote(MarketSide.BID, Decimal("100.00"), Decimal("8"), "005"),
        Quote(MarketSide.BID, Decimal("100.03"), Decimal("9"), "006"),
        Quote(MarketSide.BID, Decimal("100.06"), Decimal("2"), "007"),
        Quote(MarketSide.BID, Decimal("100.04"), Decimal("3"), "008"),
        Quote(MarketSide.BID, Decimal("100.03"), Decimal("6"), "009"),
        Quote(MarketSide.BID, Decimal("100.06"), Decimal("8"), "010"),
        Quote(MarketSide.BID, Decimal("100.00"), Decimal("1"), "011"),
        Quote(MarketSide.BID, Decimal("100.03"), Decimal("7"), "012"),
        Quote(MarketSide.BID, Decimal("100.05"), Decimal("3"), "013"),
        Quote(MarketSide.BID, Decimal("100.03"), Decimal("5"), "014"),
        Quote(MarketSide.BID, Decimal("100.00"), Decimal("9"), "015"),
    ])
    print( bidBook.topOfBook() )
    print( bidBook.removeQuote(Quote(MarketSide.BID, Decimal("20.00"), Decimal("1"), "001")) )
    print( bidBook.topOfBook() )
    print( bidBook.removeQuote(Quote(MarketSide.BID, Decimal("100.06"), Decimal("8"), "010")) )
    print( bidBook.topOfBook() )
    print( bidBook.removeQuote(Quote(MarketSide.BID, Decimal("100.06"), Decimal("2"), "007")) )
    print( bidBook.topOfBook() )
    print( bidBook.removeQuote(Quote(MarketSide.BID, Decimal("100.04"), Decimal("3"), "008")) )
    print( bidBook.topOfBook() )
    print( bidBook.removeQuote(Quote(MarketSide.BID, Decimal("100.05"), Decimal("3"), "013")) )
    print( bidBook.topOfBook() )
    print( bidBook.removeQuote(Quote(MarketSide.BID, Decimal("100.05"), Decimal("7"), "003")) )
    print( bidBook.topOfBook() )

if '__main__' == __name__:
    decimal.getcontext().prec = 10
    print( 'Testing order_book' )
    test1()
