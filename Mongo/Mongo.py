from multiprocessing import Pool
from pymongo import MongoClient
import csv
import os
import threading

lock = threading.Lock()
client = MongoClient(host='localhost', port=27017)
print(client.list_database_names())
db = client.stock

path = "../Spider/stocks"


def add_data(file):
    if not os.path.isdir(file):
        f = path + "/" + file
        ID = file[:6]
        # if ID not in db.list_collection_names():
        col = db[ID]
        with open(f, encoding='utf-8') as r:
            csv_reader = csv.reader(r)
            with lock:
                count = 0
                for row in csv_reader:
                    if count != 0:
                        col.insert_one({"Date": row[0], "Price": row[4]})
                    count = 1
        print(ID + ' finish')
        # else:
        #     print(file + ' exists')


if __name__ == '__main__':
    files = set(os.listdir(path))
    with Pool(6) as pool:
        pool.map(add_data, files)
    # collection = db.list_collection_names()
    # print(len(collection))
