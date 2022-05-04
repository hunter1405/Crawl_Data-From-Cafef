# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 10:15:36 2022

@author: ACER
"""

from selenium import webdriver
import pandas as pd
from csv import reader
import csv

url = "https://s.cafef.vn/Lich-su-giao-dich-MWG-6.chn#data"

chrome_options = Options()
chrome_options.binary_location = "C:/Users/ACER/AppData/Local/Google/Chrome SxS/Application/chrome.exe"
chrome_options.add_argument('--ignore-certificate-errors')                         
chrome_options.add_argument('--ignore-ssl-errors')                                
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])      

driver = webdriver.Chrome(chrome_options = chrome_options, executable_path='C:/Users/ACER/Downloads/crawl_cafef/chromedriver.exe') # Đường dẫn đến chromedriver (Đã set PATH))
driver.get(url=url)
time.sleep(3)

element = driver.find_element_by_name("ctl00$ContentPlaceHolder1$ctl03$dpkTradeDate1$txtDatePicker")
element.clear()
element.send_keys("11/03/2022")

search = driver.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[2]/div[1]/div[3]/div/div/div[2]/div[2]/div[2]/table/tbody/tr/td[3]/input")
search.click()

table = driver.find_element_by_id("tblData")
data = table.text

# Convert to dataframe
from io import StringIO
column = ['Date', 'Close', 'Return','Log_return','Volume','Cumulative_volume','Proportion']
df = pd.read_csv(StringIO(data), sep=" ", header = None, names=column,index_col=False)

# Clean
df = df.replace(to_replace='\(', value="", regex=True)
df = df.replace(to_replace='\)', value="", regex=True)
df = df.replace(to_replace='\%', value="", regex=True)
df["Volume"] = df["Volume"].replace(to_replace='\,', value="", regex=True).astype(float, errors = 'raise').astype(float, errors = 'raise')
df["Cumulative_volume"] = df["Cumulative_volume"].replace(to_replace='\,', value="", regex=True).astype(float, errors = 'raise').astype(float, errors = 'raise')
df['Log_return'] = df['Log_return'].astype(float, errors = 'raise')
df['Date'] = pd.to_datetime(df['Date'])

