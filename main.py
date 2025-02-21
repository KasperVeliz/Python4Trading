from universe import universe,spy
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

startingBalance = 10000
dailyGain = []
benchmarkList = []

high = startingBalance
low = startingBalance
lookback = 5
symbolData = [0] * (len(spy)-lookback)


def benchmark():
    initialBuy = startingBalance/spy.loc[lookback,'Open']
    for row in range(len(spy)-lookback):
        perShareGain = spy.loc[row+lookback,'Close'] - spy.loc[lookback,'Open']
        spyGain = perShareGain * initialBuy + startingBalance
        benchmarkList.append(spyGain)

def strategy(symbol):
    '''
    \
    :param symbol: stock ticker as string
    :return null:
    '''
    df = universe[symbol]
    pnl = 0
    index = 0

    for row in range(len(df)-lookback):

        if df.loc[row, 'Open'] > df.loc[row, 'VWAP'] or df.loc[row, 'Open'] < df.loc[row, 'VWAP']:
            perShareGain = df.loc[row+lookback, 'Close']-df.loc[row+lookback, 'Open']
            if perShareGain>0 or perShareGain<0:
                pnl += perShareGain * startingBalance/df.loc[row+lookback,'Open']
                symbolData[index] += pnl + startingBalance
                index += 1
            else:
                pnl += 0
                symbolData[index] += pnl + startingBalance
                index += 1
        else:
            pnl += 0
            symbolData[index] += 0 + startingBalance
            index += 1

print(f'Starting balance: {startingBalance}')
benchmark()
startingBalance = startingBalance/len(universe)
for stock in universe:
    strategy(str(stock))
print(f'Ending balance: {symbolData[-1]}')

x = np.linspace(0, len(symbolData), len(symbolData))
plt.plot(x,symbolData, label='Alpha Performance')
plt.plot(x,benchmarkList, label='SPY Performance')
plt.legend()
plt.xlabel('Date')
plt.ylabel('P&L')
plt.title('Daily P&L')
plt.savefig('plots/DailyP&L.png')
