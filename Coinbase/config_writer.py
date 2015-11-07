import ConfigParser

config = ConfigParser.RawConfigParser()
config.add_section("coinbase")
config.set("coinbase", "logFile",     "log.txt")
config.set("coinbase", "decimalPrec", 9)
config.set("coinbase", "clientName",  "coinbase-client-3141")
config.set("coinbase", "restApiUri",  "https://api.exchange.coinbase.com")
config.set("coinbase", "webSocket",   "wss://ws-feed.exchange.coinbase.com")
config.set("coinbase", "product",     "BTC-USD")
config.set("coinbase", "maxMove",     "200")
config.set("coinbase", "servicePort", 3141)

with open("coinbase.cfg", "wb") as configFile:
    config.write(configFile)
