import requests
import pandas as pd
import matplotlib.pyplot as plt
import csv

BASE_URL = 'https://www.alphavantage.co/query/'
API_KEY = 'IYNLLQHDNTMHS49C'

function = 'TIME_SERIES_DAILY'
output_size = 'compact'

universe = []

def get_stock_price(symbol):
    url = f'{BASE_URL}?function={function}&symbol={symbol}&outputsize={output_size}&apikey={API_KEY}'

    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        if 'Time Series (Daily)' in data:

            #data point from index
            time_series = data['Time Series (Daily)']
            dates = list(time_series.keys())
            close_prices = [float(time_series[dates]['4. close']) for dates in dates]

            data_frame = pd.DataFrame({'Date': dates, 'Price': close_prices})
            data_frame['Date'] = pd.to_datetime(data_frame['Date'])

            universe.append({symbol: data_frame})

        else:
            print(f"No data available for symbol: {symbol}")
    else:
        print("Error: API request failed")


#getting ticker symbols from s&p500tickers.csv
snp_csv = pd.read_csv('sp500_companies.csv')
snp_list = list(snp_csv['Symbol'])
symbol_list = snp_list[0:24]
for symbol in symbol_list:
    get_stock_price(symbol)
with open('s&p500tickers.csv', 'w', newline='') as csvfile:
    fieldnames = ['symbol']
    writer = csv.writer(csvfile)
    writer.writerows(universe)