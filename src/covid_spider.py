import requests
import pandas as pd
from bs4 import BeautifulSoup
from mongodb import *
import json

dbname = 'covid'
collection_name = 'cases'

date_str_to_num = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                   'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                   'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

def get_cases_data():
    url = "https://covidtracking.com/data/national/cases"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    for tr in soup.body.div.div.main.find_all('tr')[1:]:
        raw = tr.find_all('span')
        date_str, case, new_case = raw[1].contents[0], raw[3].contents[0], raw[5].contents[0]
        month_str, day, year = date_str.replace(",", "").split(" ")
        month = date_str_to_num[month_str]
        date = "{}-{}-{}".format(year, month, day)
        data.append([date, case, new_case])
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