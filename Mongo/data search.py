from pymongo import MongoClient

data1 = '1991-10-09'
data2 = '2019-11-09'
d1 = -1
d2 = -1
ID = ["000001", "000002", "000007", "000016", "000064", "000072", "000041", "000111", "000121", "000511"]
idsuggestion = ''
incre = 0
for i in ID:
    id = i
client = MongoClient(host='localhost', port=27017)
print(client.list_database_names())
db = client["stock"]
col = db["stock1"]
for id in ID:
    for x in col.find({"日期": {"$in": [data1]}, "ID": {"$in": [id]}}):
        d1 = float(x["收盘价"])
    for x in col.find({"日期": {"$in": [data2]}, "ID": {"$in": [id]}}):
        d2 = float(x["收盘价"])

    dif = d2 - d1
    dif = dif / d1
    if dif > incre:
        incre = dif
        idsuggestion = id

if d1 > 0 and d2 > 0:
    print("推荐股票id为{},增长率为{}".format(idsuggestion, incre))
elif d1 < 0 and d2 > 0:
    print("data1不是交易日")
elif d1 > 0 and d2 < 0:
    print("data2不是交易日")
elif d1 < 0 and d2 < 0:
    print("data1和data2都不是交易日")
