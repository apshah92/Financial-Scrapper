from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import py_compile




def downloadETFs(browser,url):
    browser.get(url)
    time.sleep(3)

    soup=BeautifulSoup(browser.page_source,'lxml')
    etf_table=soup.find('table',{'class':'wikitable sortable jquery-tablesorter'})
    #print(etf_table)

    etf_symbols=etf_table.find_all('a',{'class':'external text'})
    print(len(etf_symbols))
    
    etf_symbols=[symbol.text for symbol in etf_symbols]
    return etf_symbols

def writecsv(etfs,write_path):
    df=pd.DataFrame(etfs,columns=['ticker symbols'])
    df.to_csv(write_path+'Canada ETFs.csv',index=False)

if __name__=='__main__':

    py_compile.compile('Canada ETFs.py')
    url='https://en.wikipedia.org/wiki/List_of_Canadian_exchange-traded_funds#ETF_Table'
    driverpath='D:\Software Center\ARPAN SOFTWARES\chromedriver\chromedriver'  # change driverpath (path of chromedriver.exe)

    output_path='D:\Varsity Tutors\Daweili\Historical Prices- Yahoo Finance\\'
    
    browser = webdriver.Chrome(driverpath)
    list_of_etfs=downloadETFs(browser,url)
    writecsv(list_of_etfs,output_path)
    browser.close()
    

    
