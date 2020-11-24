import requests
import pandas as pd
from bs4 import BeautifulSoup
from mongodb import *
import json

dbname = "stock"
collection_name = "historical"


def get_stock_data():


def create_collection(handle):
    collection = handle[collection_name]
    collection.drop()
    print('create collection {}'.format(collection_name))
    return collection


def insert(data, handle):
    records = json.loads(data.T.to_json()).values()
    handle.insert(records)


if __name__ == "__main__":
    data = get_stock_data()
    exit()
    db = connect(dbname)
    col = create_collection(db)
    insert(data, col)
