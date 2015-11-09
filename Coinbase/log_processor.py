import sys
import re
import time
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import matplotlib
import pylab
matplotlib.rcParams.update({'font.size': 9})

def plot(bidFile, askFile, trdFile):
    bidDf = pd.read_csv(bidFile, index_col=0, parse_dates=True)
    askDf = pd.read_csv(askFile, index_col=0, parse_dates=True)
    trdDf = pd.read_csv(trdFile, index_col=0, parse_dates=True)
    # Bids in blue, Asks in red
    plt.plot(bidDf, '-b', drawstyle="steps", label="Bid")
    plt.plot(askDf, '-r', drawstyle="steps", label="Ask")
    plt.plot(trdDf, color='g', marker='o', linestyle="None", label="Trade")
    plt.title("Coinbase bid-ask")
    plt.legend(loc='lower left')
    #plt.ylim(309.6, 314.6)
    plt.show()

class UnexpectedLogFormat(Exception):
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return 'UnexpectedLogFormat[{0}]'.format(self.line)

def parseLogFile(filename):
    csvRe       = re.compile('CSV')
    lastTradeId = None
    quotes      = {
        'Bid': [],
        'Ask': [],
    }
    trades      = [] # time, price, size, isMarket
    trade       = [None, 0, 0, False, None] # time, price, size, isMarket, id
    with open(filename, 'r') as ins:
        for line in ins:
            if csvRe.search(line):
                parts     = line.split(', ')
                typeParts = parts[0].split(' - ')
                typePart  = typeParts[-1]
                if   'QUOTE_CSV' == typePart:
                    quotes[parts[2]].append((np.datetime64(parts[1]), float(parts[3]), float(parts[5])))
                elif 'TRADE_CSV' == typePart:
                    orderId = parts[6]
                    size    = float(parts[5])
                    if trade[-1] != orderId:
                        if trade[-1] is not None:
                            trades.append((trade[0], trade[1], trade[2], trade[3]))
                        trade = [np.datetime64(parts[1]), float(parts[4]), float(0), parts[3] == '1', orderId]
                    trade[2] += float(parts[5])
                else:
                    raise UnexpectedLogFormat(line)
    if trade[-1] is not None:
        trades.append((trade[0], trade[1], trade[2], trade[3]))
    tradeTimes = [x[0] for x in trades]
    tradeData  = [(x[1], x[2], x[3]) for x in trades]
    bidTimes   = [x[0] for x in quotes['Bid']]
    bidData    = [(x[1], x[2]) for x in quotes['Bid']]
    askTimes   = [x[0] for x in quotes['Ask']]
    askData    = [(x[1], x[2]) for x in quotes['Ask']]
    tradesDf = pd.DataFrame(data = tradeData, index = tradeTimes, columns = ['price', 'size', 'is_market'])
    bidsDf   = pd.DataFrame(data = bidData,   index = bidTimes,   columns = ['price', 'size'])
    asksDf   = pd.DataFrame(data = askData,   index = askTimes,   columns = ['price', 'size'])
    return {'Trades': tradesDf, 'Bids': bidsDf, 'Asks': asksDf}

def plotMarketData(data):
    bidsDf   = data['Bids']
    asksDf   = data['Asks']
    tradesDf = data['Trades']
    startTime = np.datetime64('2015-11-08T10:00:00.000000Z')
    endTime   = np.datetime64('2015-11-08T23:59:00.000000Z')
    bidsDf   = bidsDf[startTime:endTime]
    asksDf   = asksDf[startTime:endTime]
    tradesDf = tradesDf[startTime:endTime]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(bidsDf['price'], '-b', drawstyle='steps-post', label='Bid')
    ax.plot(asksDf['price'], '-r', drawstyle='steps-post', label='Ask')
    ax.plot(tradesDf['price'], 'g', marker='o', linestyle='None', label='Trade')
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%0.2f'))
    plt.title('Coinbase market data')
    plt.legend(loc='lower left')
    plt.ylim(360, 386)
    plt.show()

def tradeArrival(data):
    tradesDf = data['Trades']
    times = tradesDf.index.get_values()
    lastTime = times[0]
    dTimes = [float(times[i]-times[i-1]) for i in range(1, len(times))]
    dTimesDf = pd.DataFrame(dTimes, index = range(len(dTimes)), columns=['dTimes'])
    dTimesDf[['dTimes']].hist(bins=100)
    plt.show()

def tradeSizes(data):
    tradesDf = data['Trades']
    lastTime = None
    sizes      = []
    sizes30    = []
    sizesOther = []
    for t, d in tradesDf.iterrows():
        sizes.append(d['size'])
        if lastTime is not None:
            dt = np.datetime64(t)-lastTime
            dt = np.asscalar(dt)
            dt = dt.total_seconds()
            lastTime = np.datetime64(t)
            if (dt >= 29.0 and dt <= 31.0) or (dt >= 59.0 and dt <= 61.0):
                sizes30.append(d['size'])
            else:
                sizesOther.append(d['size'])
        else:
            lastTime = np.datetime64(t)
            sizesOther.append(d['size'])
    df30     = pd.DataFrame(sizes30, index = range(len(sizes30)), columns=['dt30'])
    dfOthers = pd.DataFrame(sizesOther, index = range(len(sizesOther)), columns=['dtOther'])
    df30[['dt30']].hist(bins=40)
    dfOthers[['dtOther']].hist(bins=40)
    plt.show()

if __name__ == "__main__":
    if 2 != len(sys.argv):
        print "Expected unique argument (configuration file)"
    else:
        logfile = sys.argv[1]
    data = parseLogFile(logfile)
    plotMarketData(data)
    #tradeArrival(data)
    #tradeSizes(data)

