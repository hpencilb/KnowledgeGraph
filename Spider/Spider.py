import re
import os
import time
import threading
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import unicodecsv as ucsv
import csv

HEADERS = {
    # 'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14'
}

lock = threading.Lock()

first_URL = 'http://quotes.money.163.com/trade/lsjysj_{code}.html'
URL = 'http://quotes.money.163.com/trade/lsjysj_{code}.html?year={year}&season={season}'
DIR_PATH = "./stocks"


def data_spider(url):
    try:
        time.sleep(0.1)
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.encoding = 'utf-8'
        bs = BeautifulSoup(r.text, 'lxml').find('table', class_="table_bg001 border_box limit_sale")
        td = bs.find_all('td')
        results = [re.findall('>(.*?)<', str(result))[0] for result in td]
        data = [results[i * 11:i * 11 + 11] for i in range(int(len(results) / 11))]
        # print(url)
        return data
    except Exception as e:
        print(e)
        time.sleep(2)
        data_spider(url)


def spider(code):
    csv_name = '{}.csv'.format(code)
    if not os.path.exists(DIR_PATH + '/' + csv_name):
        try:
            time.sleep(0.25)
            first_time = requests.get(first_URL.format(code=code), headers=HEADERS, timeout=20)
            first_time.encoding = 'utf-8'
            bs = BeautifulSoup(first_time.text, 'lxml').find('div', class_="search_area align_r")
            bs_first_year = bs.find_all('option')[-5]
            bs_last_year = bs.find_all('option')[0]
            first_year = int(re.findall('>(\\d*)<', str(bs_first_year))[0])
            last_year = int(re.findall('>(\\d*)<', str(bs_last_year))[0])
            urls = []
            for year in range(first_year, last_year + 1):
                url = [URL.format(code=code, year=year, season=season) for season in range(1, 5)]
                urls.extend(url)
            data = [['日期', '开盘价', '最高价', '最低价', '收盘价', '涨跌额', '涨跌幅(%)', '成交量(手)', '成交金额(万元)', '振幅(%)', '换手率(%)']]
            for url in urls:
                data.extend(data_spider(url))
            with lock:
                with open(DIR_PATH + '/' + csv_name, 'wb') as f:
                    w = ucsv.writer(f, encoding='utf-8')
                    w.writerows(data)
                print(code + ' finish')
        except Exception as e:
            print(e)
    else:
        print(csv_name + ' exists')


def get_code():
    data1 = []
    data2 = []
    with open('stock_industry_prep.csv') as f:
        csv_r = csv.reader(f)
        next(csv_r)
        for row in csv_r:
            data1.append(row[0])
    with open('stock_concept_prep.csv') as f:
        csv_r = csv.reader(f)
        next(csv_r)
        for row in csv_r:
            data2.append(row[0])
    data1.extend(data2)
    data = set(data1)
    return data


if __name__ == '__main__':
    if not os.path.exists(DIR_PATH):
        os.makedirs(DIR_PATH)
        print('create path ' + DIR_PATH)
    codes = get_code()
    pool = Pool(processes=4)
    try:
        pool.map(spider, codes)
    except Exception:
        time.sleep(1)
        pool.map(spider, codes)
