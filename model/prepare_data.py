import sys
sys.path.append("..")
from src.mongodb import *
import pandas as pd


def generate_data():
    db = connect('stock')
    stock_data = db['historical'].find({'code': 'AAPL'})
    stock_data = pd.DataFrame(stock_data)
    db = connect('covid')
    case_data = db['cases'].find()
    case_data = pd.DataFrame(case_data)
    df = case_data.merge(stock_data, on='date')
    df = df[['date', 'case', 'close', 'new_case']]
    period = 10
    dataset = pd.DataFrame(
        columns=['case{}'.format(i) for i in range(period)] + ['price{}'.format(i) for i in range(period)] + ['target'])
    for i in range(len(df)-period):
        case = []
        price = []
        for j in range(period):
            case.append(df['case'][i+j])
            price.append(df['close'][i+j])
        row = case + price + [df['close'][i+period]]
        dataset.loc[len(dataset.index)] = row
    return dataset


if __name__ == "__main__":
    dataset = generate_data()