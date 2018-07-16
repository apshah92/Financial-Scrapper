from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import *
from selenium.webdriver.common.keys import Keys
import xlwt
import time



driverpath='D:\Software Center\ARPAN SOFTWARES\chromedriver\chromedriver'  # change driverpath (path of chromedriver.exe)

browser= webdriver.Chrome(driverpath)

rowcount = 1
pagecount = 1

# Create excel worksheet
wb = xlwt.Workbook()
s1 = wb.add_sheet('sheet 0')

# List of Headers
headers = ['Symbol','Name']

# Write headers to excel sheet
style = xlwt.easyxf('font:bold 1')
for i in range(len(headers)):
    s1.write(0,i,headers[i],style)

sleeptime = 3
totalpages = 3
foundtp = False

try:
    while True:
        if(pagecount > totalpages):
          break
        website = "http://www.londonstockexchange.com/exchange/searchengine/search.html?lang=en&x=0&y=0&q=ETF+&page=" + str(pagecount)
        pagecount += 1
        # Open websites and download source code
        browser.get(website)
        time.sleep(sleeptime)

        soup = BeautifulSoup(browser.page_source,"lxml")

       #Get total page count
        if not foundtp:
           tp = soup.find("p",{"class":"floatsx"})
           print(tp)
           totalpages=int(tp.text.split()[-1])
           foundtp = True

        main_table=soup.find(id='contentIndex')
        rows=main_table.find_all('tr',{'class':'odd'})
        rows+=main_table.find_all('tr',{'class':'even'})

        for i in range(len(rows)):
            data=rows[i].find_all('td',{'class':'name'})[:2]            
            for col in range(len(data)):
                try:
                    s1.write(rowcount,col,data[col].text)
                except:
                    s1.write(rowcount,col,'')
            rowcount+=1
except Exception as e:
    print(e)
    # Save the excel sheet with given name
    wb.save('London ETFs.xls')

wb.save('London ETFs.xls')
browser.close()
    
        
    
    


    
