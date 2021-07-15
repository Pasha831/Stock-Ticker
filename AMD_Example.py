import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

amd = yf.Ticker('AMD')  # making a Ticker class to work with it
amd_info = amd.info  # all usefull info about AMD stocks

# print(amd_info)
print(amd_info['country'])
print(amd_info['sector'])
print(amd_info['ebitda'], '\n')

amd_share_price_data = amd.history(period='max')  # data about price of AMD from it's beginning, pandas Dataframe
amd_share_price_data.reset_index(inplace=True)  # replace first header with null indexes

plt.plot(amd_share_price_data['Date'], amd_share_price_data['Open'], marker='o')  # making a polt
plt.xlabel('Date')
plt.ylabel('Open price, $')
plt.show()