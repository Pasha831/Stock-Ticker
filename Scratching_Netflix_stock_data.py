import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html'
data = requests.get(url).text

soup = BeautifulSoup(data, 'html5lib')

netflix_data = pd.DataFrame(columns=['Date',
                                     'Open',
                                     'High',
                                     'Low',
                                     'Close',
                                     "Adj Close",
                                     'Volume'])
t_body = soup.find('tbody')

for row in t_body.find_all('tr'):
    cells = row.find_all('td')
    date = cells[0].text
    open = cells[1].text
    high = cells[2].text
    low = cells[3].text
    close = cells[4].text
    adj_close = cells[5].text
    volume = cells[6].text

    netflix_data = netflix_data.append({'Date':date,
                                        'Open':open,
                                        'High':high,
                                        'Low':low,
                                        'Close':close,
                                        "Adj Close":adj_close,
                                        'Volume':volume}, ignore_index=True)

# print(netflix_data.head(10))


# or... not the best way: a lot of space and trash in it
# read_html_pandas_data = pd.read_html(url)
# netflix_dataframe = read_html_pandas_data[0]
# print(netflix_dataframe)