import requests
import pandas as pd
from bs4 import BeautifulSoup
from mongodb import *
import json

dbname = 'covid'

date_str_to_num = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                   'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                   'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

def get_cases_data(db=None):
    url = "https://covidtracking.com/data/national/cases"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    for tr in soup.body.div.div.main.find_all('tr')[1:]:
        raw = tr.find_all('span')
        date_str, case, new_case = raw[1].contents[0], int(raw[3].contents[0].replace(',','')), int(raw[5].contents[0].replace(',',''))
        month_str, day, year = date_str.replace(",", "").split(" ")
        month = date_str_to_num[month_str]
        date = pd.to_datetime("{}-{}-{}".format(year, month, day))
        data.append([date, case, new_case])
    df = pd.DataFrame(data=data, columns=['date','case','new_case'])
    if db is not None:
        col = create_collection(db, 'cases')
        insert(df, col)
    return df


def get_states_data(db=None):
    url = "https://data.cdc.gov/resource/9mfq-cb36.json"
    response = requests.get(url)
    res = json.loads(response.text)
    df = pd.DataFrame(res)
    dates = [df['submission_date'].loc[i].split('T')[0] for i in range(len(df['submission_date']))]
    df['date'] = pd.to_datetime(dates)
    if db is not None:
        col = create_collection(db, 'states')
        insert(df, col)
    return df


def create_collection(handle, collection_name):
    collection = handle[collection_name]
    collection.drop()
    print('create collection {}'.format(collection_name))
    return collection


def insert(data, handle):
    records = json.loads(data.T.to_json()).values()
    handle.insert(records)


if __name__ == "__main__":
    db = connect(dbname)
    cases_data = get_cases_data(db)
    states_data = get_states_data(db)