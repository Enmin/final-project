import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://finance.yahoo.com/quote/AAPL/history?p=AAPL'

def get_data(url):
    data = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    stockTable = soup.find('table', attrs={'class': 'W(100%) M(0)'})
    stockInfo = stockTable.find_all('tr', attrs={'class': 'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)'})
    for info in stockInfo:
        d = info.find_all('span')
        if len(d) == 7:
            data.append([d[i].text for i in range(len(d))])
    df = pd.DataFrame(data = data, columns= ['Date','Open','High','Low','Close','Adj Close','Volume'])
    return df

if __name__ == '__main__':
    get_data(url)