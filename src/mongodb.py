from pymongo import MongoClient

connection_string = "mongodb+srv://enmin:data1050@sandbox.skbnz.mongodb.net/test"


def connect(db):
    client = MongoClient(connection_string)
    return client[db]


if __name__ == '__main__':
    connect('admin')