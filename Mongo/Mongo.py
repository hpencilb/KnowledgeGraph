import time
from multiprocessing import Pool
from pymongo import MongoClient
import csv
import os
import threading

lock = threading.Lock()
client = MongoClient(host='localhost', port=27017)
print(client.list_database_names())
db = client["stock"]
col = db["data"]
path = "stocks"


def add_data(file):
    if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
        f = path + "/" + file  # 打开文件
        id = file[:6]
        print(id)
        with open(f, encoding='utf-8') as r:
            csv_reader = csv.reader(r)
            count = 0
            for row in csv_reader:
                if count != 0:
                    with lock:
                        col.insert_one({"ID": id, "日期": row[0], "收盘价": row[4]})
                count = 1


if __name__ == '__main__':
    files = set(os.listdir(path))
    with Pool(4) as pool:
        pool.map(add_data, files)
