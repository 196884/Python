def defEnum( *args ):
    tags = [ x.upper() for x in args ]
    vals = [ x[0].upper() + x[1:].lower() for x in args ]
    res = dict( zip( tags, vals ) )
    return type( "Enum", (), res )

MarketSide  = defEnum( 'BID', 'ASK' )
OrderSide   = defEnum( 'BUY', 'SELL' )
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


