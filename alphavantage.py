import requests
import pandas as pd
import matplotlib.pyplot as plt

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
function = 'TIME_SERIES_DAILY'
symbol = 'IBM'
url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize=compact&apikey=IYNLLQHDNTMHS49C'
r = requests.get(url)
data = r.json()

print(data)

raw = data.get('Time Series (Daily)', {})
x = list(raw.keys())
print(x)
y = []
for select, obj in raw.items():
    for attr in obj:
        if attr == '4. close':
            y.append(obj[attr])

print(y)
plt.plot(x, y)
plt.title(f'{symbol} Price History')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.show()