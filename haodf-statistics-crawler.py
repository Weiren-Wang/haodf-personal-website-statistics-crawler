from bs4 import BeautifulSoup
from selenium import webdriver
import re
import sys
import os
import requests
from bs4 import BeautifulSoup   
import urllib
import xlwt  
import sqlite3 
import xlrd
import pandas as pd
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
                data_dict[list(data_dict.keys())[i+1]].append(value)
            data_dict['url'].append(url)
            res = pd.concat([res,pd.DataFrame(data_dict)],axis = 0)
            if x%10 == 0:
                print(res)
        except:
            bug_url.append(url)
            print('Skip url index : ',x)
            continue
    res.to_csv('./crawled_data.csv')

if __name__=="__main__":


    main()