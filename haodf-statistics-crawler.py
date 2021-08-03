from bs4 import BeautifulSoup
from selenium import webdriver
import re
import sys
import os
import requests
from bs4 import BeautifulSoup   #bs4正则表达式进行文字匹配
import urllib
import xlwt  #进行Excel操作
import sqlite3 #数据库
import xlrd
import pandas as pd
import numpy as np
import os
import webbrowser
import lxml

import ssl

def main():
    bug_url = []

    wb = xlrd.open_workbook("durl_y.xls")
    sht = wb.sheet_by_name("Sheet1")
    res = pd.DataFrame(columns = ['name', 'js-total-new-pv', 'js-yesterdayCnt', 'js-patientSigninCnt', 'js-articleCount', 'js-spaceRepliedCount', 'js-diagnosis-report', 'js-wxdiagnosis-report', 'js-totaldiagnosis-report', 'js-doctorVoteCnt', 'js-thankLetterCount', 'js-presentCnt', 'js-spaceActiveDate', 'js-openSpaceTime', 'url'])
    driver = webdriver.Firefox()
    driver.maximize_window()

    for x in range(sht.nrows):
        url=str(sht.cell(x,0).value)
        try:
            data_dict = {'name':[],'js-total-new-pv':[],'js-yesterdayCnt':[],'js-patientSigninCnt':[],
                      'js-articleCount':[],'js-spaceRepliedCount':[],'js-diagnosis-report':[],
                      'js-diagnosis-report':[],'js-wxdiagnosis-report':[],'js-totaldiagnosis-report':[],
                      'js-doctorVoteCnt':[],'js-thankLetterCount':[],'js-presentCnt':[],
                      'js-spaceActiveDate':[],'js-openSpaceTime':[],'url':[]}
            driver.get(url)
            data = driver.page_source
            soup = BeautifulSoup(data,'lxml')
            name_string = str(soup.find_all('h1',class_="doctor-name"))
            name_match_rule = re.compile(r'<h1 class="doctor-name">(.*?)</h1>')
            name=re.findall(name_match_rule,name_string)[0]
            data_dict['name'].append(name)
            for i,item in enumerate(soup.find_all('span',class_="per-sta-data")):

                item=str(item)
                match_str = '<span class="per-sta-data ' + str(list(data_dict.keys())[i+1]) + '">(.*?)</span>'
                match_rule = re.compile(match_str)
                value = re.findall(match_rule,item)[0]
                if str(list(data_dict.keys())[i + 1]) == 'js-total-new-pv':
                    if not value:
                        for j in range(10):
                            driver.get(url)
                            data = driver.page_source
                            soup = BeautifulSoup(data, 'lxml')
                            item = str(soup.find_all('span',class_="per-sta-data")[0])
                            match_str = '<span class="per-sta-data ' + 'js-total-new-pv' + '">(.*?)</span>'
                            match_rule = re.compile(match_str)
                            value = re.findall(match_rule, item)[0]
                            if value:
                                break
                data_dict[list(data_dict.keys())[i+1]].append(value)
            data_dict['url'].append(url)
            if x%10 == 0:
                print('目前爬取量：',x,'/',sht.nrows)
            res = pd.concat([res, pd.DataFrame(data_dict)], axis=0)
        except:
            data_dict = {'name': np.nan, 'js-total-new-pv': np.nan, 'js-yesterdayCnt': np.nan, 'js-patientSigninCnt': np.nan,
             'js-articleCount': np.nan, 'js-spaceRepliedCount': np.nan, 'js-diagnosis-report': np.nan,
             'js-diagnosis-report': np.nan, 'js-wxdiagnosis-report': np.nan, 'js-totaldiagnosis-report': np.nan,
             'js-doctorVoteCnt': np.nan, 'js-thankLetterCount': np.nan, 'js-presentCnt': np.nan,
             'js-spaceActiveDate': np.nan, 'js-openSpaceTime': np.nan, 'url': url}
            res = pd.concat([res, pd.DataFrame(data_dict,index = [0])], axis=0)
            continue
    res.to_csv('./crawled_data.csv')

if __name__=="__main__":


    main()