import time
import unicodecsv as ucsv
from bs4 import BeautifulSoup
import os
import re

DIR_PATH = "./stockpage"
year_founded = [['code', 'name', 'year_founded']]
year_listed = [['code', 'name', 'year_listed']]


def get_files():
    files = os.listdir(DIR_PATH)
    File = [DIR_PATH + '/' + file for file in files]
    return File


def add_data(file_path):
    try:
        with open(file_path, 'r', encoding="gbk") as f:
            raw = f.read()
        bs = BeautifulSoup(raw, 'lxml')
        head = bs.find('div', class_="code fl").find('a', href="./")
        name = re.findall('title="(.*?)\\s', str(head))[0]
        code = re.findall('title=.*?\\s(\\d*)', str(head))[0]
        year = bs.find('div', class_="m_box company_detail").find('table', class_="m_table").find_all('tr')
        founded = re.findall('<span>(.*?)-', str(year[0].find_all('td')[0]))[0]
        listed = re.findall('<span>(.*?)-', str(year[1].find_all('td')[0]))[0]
        year_founded.extend([[code, name, founded]])
        year_listed.extend([[code, name, listed]])
        print(file_path + ' finish')
    except Exception as e:
        print(e)
        print(file_path + ' has problem')


if __name__ == '__main__':
    file_list = set(get_files())
    # file_list = get_files()
    # add_data(file_list[0])
    for File in file_list:
        add_data(File)
    # print(year_listed)
    print(year_listed)
    print(year_founded)
    with open('Year_Founded.csv', 'wb') as f:
        w = ucsv.writer(f, encoding='utf-8')
        w.writerows(year_founded)
    with open('Year_Listed.csv', 'wb') as f:
        w = ucsv.writer(f, encoding='utf-8')
        w.writerows(year_listed)
