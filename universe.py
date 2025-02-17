import pandas as pd
from alpaca.data import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
from datetime import datetime

from alpaca_api_info import API_KEY, API_SECRET

client = StockHistoricalDataClient(API_KEY, API_SECRET)


#Pull & process ticker names from sp500_companies.csv (sorted by weight)
def flattenList(nested_list):
    flat_list = []
    for sublist in nested_list:
        for item in sublist:
            flat_list.append(item)
    return flat_list

csvTickers = pd.read_csv('sp500_companies.csv', usecols=['Symbol'])
tickerList = flattenList(csvTickers.values)

#Fetch data from Alpaca API and create pandas dataframe
#Add key (symbol) to universe, then add corresponding dataframe as value

universe = {}
def dataProcessing(symbol):
    try:
        requstParam = StockBarsRequest(symbol_or_symbols=symbol,
                                       timeframe=TimeFrame.Day,
                                       start=datetime(2022,1,1),
                                       end=datetime(2025,1,1)
                                       )
        bars = client.get_stock_bars(requstParam)
        bars = pd.DataFrame(bars[symbol])
        bars.columns = ['Symbol','Date','Open','High','Low','Close','Volume','Trade Count','VWAP']
        #Pull value from tuple and add to dataframe
        for row in list(range(len(bars))):
            bars.loc[row,'Date'] = bars['Date'][row][1].date()
            bars.loc[row,'Symbol'] = bars['Symbol'][row][1]
            bars.loc[row,'Open'] = bars['Open'][row][1]
            bars.loc[row,'High'] = bars['High'][row][1]
            bars.loc[row,'Low'] = bars['Low'][row][1]
            bars.loc[row,'Close'] = bars['Close'][row][1]
            bars.loc[row,'Volume'] = bars['Volume'][row][1]
            bars.loc[row,'Trade Count'] = bars['Trade Count'][row][1]
            bars.loc[row,'VWAP'] = bars['VWAP'][row][1]
        return bars
    except Exception as e:
        print(f'Error: {e}')

for symbol in tickerList:
    universe.update({symbol: dataProcessing(symbol)})

spy = dataProcessing('SPY')