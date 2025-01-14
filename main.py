import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import yahoo_fin.stock_info as si

style.use('ggplot')
start = dt.datetime(2020, 1, 1)
end = dt.datetime(2024, 12, 31)

snp_list = si.tickers_sp500()
print("tickers sp500: " + str(len(snp_list)))
print(snp_list[0:10])