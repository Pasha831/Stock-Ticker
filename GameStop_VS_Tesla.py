import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# functions to make a graph
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


### Work with Tesla ###

tesla = yf.Ticker('TSLA')
tesla_data = tesla.history(period='max')
tesla_data.reset_index(inplace=True)
# print(tesla_data.head(5))

url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
html_data_T = requests.get(url).text  # T - means Tesla
beautiful_soup = BeautifulSoup(html_data_T, 'html5lib')

tables = beautiful_soup.find_all('table')  # all tables on this page
index = 0  # to find index of the table that we need
# print(tables)

for i in range(len(tables)):
    if 'Tesla Quarterly Revenue' in str(tables[i]):
        index = i  # find it
        break  # quit it

# print(tables[index].prettify())  # beautiful view of the table :)
t_body = tables[index].find('tbody')
# print(t_body.prettify())  # beautiful view of the table body :)

# making a Pandas Dataframe with Date and Revenue columns
tesla_revenue = pd.DataFrame(columns=['Date',
                                      'Revenue'])

rows = t_body.find_all('tr')  # all rows in our table
for row in rows:
    cells = row.find_all('td')  # all cells in each row: date and revenue

    date = cells[0].text
    revenue = cells[1].text

    # adding values to Dataframe
    tesla_revenue = tesla_revenue.append({'Date':date,
                                          'Revenue':revenue}, ignore_index=True)

# print(tesla_revenue)  # see the magic :D

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")  # replace , and $ with '' space

# remove missing values
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
# print(tesla_revenue)

### End of work with Tesla ###


### Starting work with GameStop ###

gme = yf.Ticker('GME')  # ticker for GameStop
gme_data = gme.history(period='max')
gme_data.reset_index(inplace=True)
# gme_data.head()  # first 5 rows of a DF

url = 'https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue'
html_data_G = requests.get(url).text  # G - means GameStop

beautiful_soup = BeautifulSoup(html_data_G, 'html5lib')

gme_revenue = pd.DataFrame(columns=['Date',
                                    'Revenue'])

tables = beautiful_soup.find_all('table')
index = 0
for i in range(len(tables)):
    if 'GameStop Quarterly Revenue' in str(tables[i]):
        index = i  # it's 1
        break

t_body = tables[index].find('tbody')
# print(t_body.prettify())

rows = t_body.find_all('tr')
for row in rows:
    cells = row.find_all('td')

    date = cells[0].text
    revenue = cells[1].text

    gme_revenue = gme_revenue.append({'Date':date,
                                    'Revenue':revenue}, ignore_index=True)

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")  # replace , and $ with '' space

# remove missing values
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
# print(gme_revenue)

### End work with GameStop ###

### Plotting the graphs ###
# make_graph(tesla_data, tesla_revenue, 'Tesla')
# make_graph(gme_data, gme_revenue, 'GameStop')
