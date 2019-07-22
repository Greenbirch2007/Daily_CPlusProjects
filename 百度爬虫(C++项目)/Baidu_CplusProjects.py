# -*- coding:utf8 -*-



# 写个小脚本就搞定了！
import re

import pymysql

import time
from selenium import webdriver
from lxml import etree
import datetime

driver = webdriver.Chrome()


# 请求

def get_first_page():
    url = 'https://www.baidu.com/s?wd=c%2B%2B%E9%A1%B9%E7%9B%AE&rsv_spt=1&rsv_iqid=0xd4d51f19000f3f6a&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=1&rsv_t=354c9o3eHFdpdsBOaQaviEedTBLlMeg1j47HwYPPJE52By9KoxCxaP2ppBkgaDaZMV8j&oq=%25E6%2597%25A5%25E7%25BB%258F%25E6%258C%2587%25E6%2595%25B0&inputT=3853&rsv_pq=9cd76e1d000ac6b8&rsv_sug1=22&rsv_sug7=100&rsv_sug3=17&sug=cpa&rsv_n=1&bs=c%2B%2B%E9%A1%B9%E7%9B%AE&rsv_jmp=fail'
    driver.set_window_size(1200, 1200)  # 设置窗口大小
    driver.get(url)
    # time.sleep(3)
    html = driver.page_source
    # time.sleep(3)
    return html


def next_page():

    for i in range(1, 666):  # selenium 循环翻页成功！
        try:

            driver.find_element_by_xpath('//*[@id="page"]/a[last()]').click()
            html = driver.page_source
            return html
        except:
            print("先略过～")


# 用遍历打开网页59次来处理

# print(html)  #正则还是有问题，选择了一个动态变动的颜色标记是不好的 最近浏览不是每次都有的！所以用数字的颜色取判断吧

def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    try:
        big_list =[]
        patt = re.compile('<div class="c-tools" id=".*?" data-tools="{&quot;title&quot;:&quot;(.*?)&quot;,&quot;url&quot;:&quot;(.*?)">',re.S)
        items = re.findall(patt,html)
        for item in items:
            big_list.append(item)
        return big_list
    except:
        print("先略过～")




# 存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='D_CPlus',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into Baidu_CPlusProjects (title,link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass

if __name__ == '__main__':
    html = get_first_page()
    content = parse_html(html)
    insertDB(content)
    while True:
        time.sleep(1)
        html = next_page()
        content = parse_html(html)
        insertDB(content)
        print(datetime.datetime.now())
    #

#
# create table Baidu_CPlusProjects(
# id int not null primary key auto_increment,
# title text,
#  link text
# ) engine=InnoDB  charset=utf8;


#  drop table Baidu_CPlusProjects;








