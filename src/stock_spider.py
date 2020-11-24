import requests
import pandas as pd
from datetime import datetime
from mongodb import *
import json

dbname = "stock"
collection_name = "historical"

url = 'https://query1.finance.yahoo.com/v8/finance/chart/{}'


def get_stock_data(code):
    period = "1y"
    interval = "1d"
    params = {}
    params["range"] = period
    params["interval"] = interval.lower()
    res = requests.get(url.format(code), params=params)
    res_json = json.loads(res.text)
    data = res_json['chart']['result'][0]
    timestamps = data['timestamp']
    date = [datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d') for timestamp in timestamps]
    indicators_data = data['indicators']['quote'][0]
    volume = indicators_data['volume']
    close = indicators_data['close']
    open = indicators_data['open']
    high = indicators_data['high']
    low = indicators_data['low']
    df = pd.DataFrame({'date':date, 'volume':volume, 'close':close, 'open':open, 'high': high, 'low':low})
    return df


def create_collection(handle):
    collection = handle[collection_name]
    collection.drop()
    print('create collection {}'.format(collection_name))
    return collection


def insert(data, handle):
    records = json.loads(data.T.to_json()).values()
    handle.insert(records)


if __name__ == "__main__":
    data = get_stock_data('AAPL')
    db = connect(dbname)
    col = create_collection(db)
    insert(data, col)
