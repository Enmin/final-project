import requests
import pandas as pd
from bs4 import BeautifulSoup
from mongodb import *
import json

dbname = 'covid'
collection_name = 'cases'


def get_cases_data():
    url = "https://covidtracking.com/data/national/cases"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    for tr in soup.body.div.div.main.find_all('tr')[1:]:
        raw = tr.find_all('span')
        data.append([raw[1].contents[0], raw[3].contents[0], raw[5].contents[0]])
    df = pd.DataFrame(data=data, columns=['Date','Case','new_case'])
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
    data = get_cases_data()
    db = connect(dbname)
    col = create_collection(db)
    insert(data, col)