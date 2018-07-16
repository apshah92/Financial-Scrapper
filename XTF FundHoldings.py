from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import *
from selenium.webdriver.common.keys import Keys
import pandas
import xlwt
import time
import re



def launchurl(url,driverpath):
    browser = webdriver.Chrome(driverpath)
    browser.get(url)
    time.sleep(2)

    #give time to close the pop up
    time.sleep(8)

    return browser



def downloadFundHoldings(browser):
    '''
    steps:    
    1.launch url
    2.click fundholdings tab
    3.parsse html to soup object
    4.find maintable
        
    5.iterate row wise under maintable
    6.find column data 0,2 under each row and store each text in a list of lists -data= [[ , ],[ , ],[ , ],..]
    7.switch back to other tab
    '''

    df=pandas.read_excel('ETF ratings.xls',header=0)
    
    etfs=df.values.transpose().tolist()[0]
    print(etfs[:10])
    
    fund_holdings_url='http://www.xtf.com/ETF-Ratings/'
    browser.get(fund_holdings_url) #1
    time.sleep(3)

    wb = xlwt.Workbook()        
    s2 = wb.add_sheet('sheet 0')

    headers=['Symbol','Weight']

    for i in range(len(headers)):
        s2.write(0,i,headers[i])
    
    
    tabsPanel_id='ctl00_Main_RatingsTabs_TC'
    fundholdings_id='ctl00_Main_RatingsTabs_T2'
    ative_fundholdings_id='ctl00_Main_RatingsTabs_AT2'
    maintable_id='ctl00_Main_RatingsTabs_ctl46_grdListOfETFs_DXMainTable'
    headerrow_id='ctl00_Main_RatingsTabs_ctl46_grdListOfETFs_DXHeadersRow0'
    symbolcol_id='ctl00_Main_RatingsTabs_ctl46_grdListOfETFs_col0'
    weightcol_id='ctl00_Main_RatingsTabs_ctl46_grdListOfETFs_col2'
    row_id='ctl00_Main_RatingsTabs_ctl46_grdListOfETFs_DXDataRow'
    
    rowdata_class='dxgv' #used to get column data in a row


    rowcount=1    
    for etf in etfs:
        print(etf)
        try:
            browser.get(fund_holdings_url+etf) #1
            time.sleep(2)

            try:        
                fundholdings_tab=browser.find_element_by_id(fundholdings_id)
                fundholdings_tab.click()#2
                time.sleep(1.5)
            except:
                fundholdings_tab=browser.find_element_by_id(ative_fundholdings_id)
                fundholdings_tab.click()#2
                time.sleep(1.5) 

            soup2=BeautifulSoup(browser.page_source,'lxml') #3
            maintable_soup=soup2.find(id=maintable_id)#4

            number_of_rows=len(maintable_soup.find_all(id=re.compile('^'+row_id)))
            print(number_of_rows)

            if number_of_rows<5:
                n=len(maintable_soup.find_all(id=re.compile('^'+row_id)))
            else:
                n=5
            
            rowdata=[]
            for i in range(n):
                row=maintable_soup.find(id=row_id+str(i)) #5
                
                rowdata=[row.find_all('td',{'class':rowdata_class})[j] for j in (0,2)] #6 [x:y:z] start -x end-y step -z
                
                for i in range(len(rowdata)):
                    try:
                        s2.write(rowcount,i,rowdata[i].text)
                    except:
                        print(etf)
                        s2.write(rowcount,i,"")
                rowcount+=1
        except Exception as e:
            print(e)
            
            
        
    wb.save('XTF fundholdings.xls')           



if __name__=='__main__':
    url="http://www.xtf.com/ETF-Explorer"
    driverpath='D:\Software Center\ARPAN SOFTWARES\chromedriver\chromedriver'


    browser=launchurl(url,driverpath)
    downloadFundHoldings(browser)

    browser.close()
    

