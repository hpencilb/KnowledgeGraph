from pymongo import MongoClient

date1 = '2019-11-19'
date2 = '2019-12-19'
max_num = 5


class RecommendStock:
    def __init__(self, Stock_list):
        self.stock_list = Stock_list
        self.client = MongoClient(host='localhost', port=27017)
        self.d1 = []
        self.d2 = []

    def find_best(self):
        ID_list = self.stock_list
        Dif = []
        stock = []
        db = self.client["stock"]
        for ID in ID_list:
            col = db[ID]
            for x in col.find({"日期": {"$in": [date1]}}):
                self.d1.append(float(x["收盘价"]))

            for x in col.find({"日期": {"$in": [date2]}}):
                self.d2.append(float(x["收盘价"]))
            dif = self.d2[-1] - self.d1[-1]
            dif = dif / self.d1[-1]
            Dif.append(dif)
        suggestion = Dif[:]
        suggestion.sort(reverse=True)
        for i in suggestion:
            n = Dif.index(i)
            stock.append(ID_list[n])
            Dif[n] = -100000
        Sug = []
        for i in range(len(Dif)):
            string = stock[i] + ' 增长率为:' + str(round(suggestion[i], 4))
            Sug.append(string)
        answer = '根据最近一个月的增长率,推荐的股票代码是: ' + '; '.join(Sug[:max_num])
        return [str(answer)]


if __name__ == '__main__':
    stock_list = ["000001", "000002", "000003", "000004", "000005", "000006", "000007", "000008", "000009", "000010"]
    r = RecommendStock(stock_list)
    print(r.find_best())
