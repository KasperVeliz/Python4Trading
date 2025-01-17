import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import yahoo_fin.stock_info as si
import backtrader as bt
from pandas_datareader.wb import download

style.use('ggplot')
start = dt.datetime(2020, 1, 1)
end = dt.datetime(2024, 12, 31)

dow_list = si.tickers_dow()
historical_datas = {}
for ticker in dow_list:
    historical_datas[ticker] = si.get_data(ticker, start_date=start, end_date=end, interval='1d')

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(10000)
    data = bt.feeds.PandasData
    cerebro.adddata(dow_list)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())