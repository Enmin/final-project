import sys
sys.path.append("..")
# from src.mongodb import *
from src.mongodb import *
import pandas as pd

def get_covid_case():
    # get covid data from MongoDB
    connection_string = "mongodb+srv://enmin:data1050@sandbox.skbnz.mongodb.net/test"
    client = MongoClient(connection_string)
    db = client.get_database("covid")
    collection = db.get_collection("cases")
    data = list(collection.find())
    covid_df = pd.DataFrame.from_records(data)
    covid_df.drop('_id', axis=1, inplace=True)
    covid_df['date'] = pd.to_datetime(covid_df['date'])
    return covid_df

def get_stock_data():
    connection_string = "mongodb+srv://enmin:data1050@sandbox.skbnz.mongodb.net/test"

    client = MongoClient(connection_string)
    db = client.get_database("stock")
    collection = db.get_collection("historical")
    data = list(collection.find())
    stock_df = pd.DataFrame.from_records(data)
    stock_df.drop('_id', axis=1, inplace=True)
    stock_df['date'] = pd.to_datetime(stock_df['date'])
    stock_df = stock_df.dropna()

    # create a new column in stock_df to show price fluctuation
    # columns = ['AAPL', 'MSFT', 'GOOG', 'FB', 'AMZN', 'WMT', 'GE', 'MMM', 'AMT', 'JNJ', 'PFE', 'JPM', 'V', 'XOM', '^GSPC', '^DJI', 'GC=F', 'CL=F']
    codes = stock_df['code'].unique()
    fluc = dict()
    for code in codes:
        fluc[code] = [0] + [(stock_df[stock_df['code']==code].iloc[i]['close'] - stock_df[stock_df['code']==code].iloc[i-1]['close'])/stock_df[stock_df['code']==code].iloc[i-1]['close']
                            for i in range(1,stock_df[stock_df['code']==code]['date'].nunique())]
    record = []
    for code in codes:
        record += fluc[code]
    stock_df['fluctuation'] = record
    return stock_df


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
        columns=['case{}'.format(i) for i in range(period)] + ['price{}'.format(i) for i in range(period)] + ['date'] + ['target'])
    for i in range(len(df)-period):
        case = []
        price = []
        for j in range(period):
            case.append(df['case'][i+j])
            price.append(df['close'][i+j])
        row = case + price + [df['date'][i+period]] + [df['close'][i+period]]
        dataset.loc[len(dataset.index)] = row
    return dataset


if __name__ == "__main__":
    dataset = generate_data()
    print(dataset.shape)
    # print(dataset.columns)