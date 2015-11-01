import ConfigParser

config = ConfigParser.RawConfigParser()
config.add_section("coinbase")
config.set("coinbase", "clientName", "coinbase-client-3141")
config.set("coinbase", "restApiUri", "https://api.exchange.coinbase.com")
config.set("coinbase", "webSocket", "wss://ws-feed.exchange.coinbase.com")
config.set("coinbase", "logFile", "log.txt")
config.set("coinbase", "priceLowerBound", 280)
config.set("coinbase", "priceUpperBound", 380)
config.set("coinbase", "priceResolution", 0.01)

with open("coinbase.cfg", "wb") as configFile:
    config.write(configFile)
