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


def downloadData(browser):   
    soup=BeautifulSoup(browser.page_source,'lxml')
    ratingTable=soup.find(id='ctl00_Main_ASPxGridViewETFs_DXMainTable')    #parent tag to find  descendent data tags
    
    headers=[]
    for i in (0,1,2,5,10,11):
        headers.append(ratingTable.find(id='ctl00_Main_ASPxGridViewETFs_col'+str(i)).text)

    
    wb = xlwt.Workbook()        
    s1 = wb.add_sheet('sheet 0')
    
    for i in range(len(headers)):
        s1.write(0,i,headers[i])

    
    
    bottomPanel=browser.find_element_by_id('ctl00_Main_ASPxGridViewETFs_DXPagerBottom')
    pageNext=bottomPanel.find_element_by_class_name('dxWeb_pNext_XTF')
    pagebuttonSoup=soup.find('img',{'class':'dxWeb_pNext_XTF'})
    
    print(pagebuttonSoup['class'])
    print(pageNext)

    etfSymbols=[]
    rowcount=1

    
    while pagebuttonSoup['class']==['dxWeb_pNext_XTF']:
        soup=BeautifulSoup(browser.page_source,'lxml')        
        nextButtonDisabled=soup.find('img',{'class':'dxWeb_pNextDisabled_XTF'})
        if nextButtonDisabled!=None:
            pagebuttonSoup=nextButtonDisabled

        ratingTable=soup.find(id='ctl00_Main_ASPxGridViewETFs_DXMainTable')    #parent tag to find  descendent data tags

        rows=ratingTable.find_all(id=re.compile('^ctl00_Main_ASPxGridViewETFs_DXDataRow'))

        #print(len(rows))        

        for i in range(len(rows)):
            coldata=[rows[i].find_all('td',{'class':'dxgv'})[j] for j in (0,1,2,4,6,7)]
            coldata[0]=coldata[0].find('a')
            
            etfSymbols.append(coldata[0].text)         
            #print('coldata:',coldata)
            for j in range(len(coldata)):
                s1.write(rowcount,j,coldata[j].text)
                #print(coldata[j].text)
            rowcount+=1
        try:
            pageNext=browser.find_element_by_class_name('dxWeb_pNext_XTF')
            pageNext.click()
            time.sleep(1.5)
        except Exception as e:
            print(e)            
            wb.save('ETF ratings.xls')
            return etfSymbols

    wb.save('ETF ratings.xls') 
    return etfSymbols


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
    try:
        for etf in etfs:
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
                    s2.write(rowcount,i,rowdata[i].text)
                rowcount+=1
        except Exception as e:
            print(e)
            wb.save('XTF fundholdings.xls')
        
    wb.save('XTF fundholdings.xls')           



if __name__=='__main__':
    url="http://www.xtf.com/ETF-Explorer"
    driverpath='D:\Software Center\ARPAN SOFTWARES\chromedriver\chromedriver'


    browser=launchurl(url,driverpath)
    #etfSymbols=downloadData(browser)
    downloadFundHoldings(browser)

    browser.close()
    

