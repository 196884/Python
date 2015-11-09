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

if __name__ == "__main__":
    bidFile = "bids.csv"
    askFile = "asks.csv"
    trdFile = "trades.csv"
    plot(bidFile, askFile, trdFile)
