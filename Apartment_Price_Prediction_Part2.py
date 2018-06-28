# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 00:37:46 2018

@author: Bantee Rathor
"""





#  SCARPPING DATA FROM MAKAN.COM

import urllib2
from bs4 import BeautifulSoup as bs
url_1 = "https://www.makaan.com/jaipur-residential-property/rent-property-in-jaipur-city"


location=[]
area=[]
BHK=[]
price = []


for i in range(100):
    
    url='https://www.makaan.com/jaipur-residential-property/rent-property-in-jaipur-city?page='+str(i)
    page=urllib2.urlopen(url)
    soup=bs(page,"lxml")
    all_div = soup.find_all('div',class_ = "infoWrap")


    #BHK
    for section in all_div:
        info = section.find_all('div',class_="title-line")
        n_raw = info[0].text.strip()
        n_raw=int(n_raw[0])
        BHK.append(n_raw) 
    
    #location
    for section in all_div:
        info = section.find_all('div',class_="locWrap")
        n_raw = info[0].text.strip()
        n_raw=n_raw.split(',')
        n_raw=n_raw[0]
        location.append(n_raw)

    #price
    for section in all_div:
        info = section.find_all('div',class_="price")
        n_raw=info[0].text.strip().replace(',','')
        n_raw = n_raw.split()
        if len(n_raw) == 3 and n_raw[1].lower() in ['lac','lacs','lakh','lakhs']:
                price.append(int(float(n_raw[0])*100000))
        else:
                price.append(int(float(n_raw[0])))
       
    
#area
    for section in all_div:
        info = section.find_all('div',class_="size")
        n_raw=info[0].text.strip()
        area.append(n_raw)
    

#Making the dataframe
import pandas as pd
df1 = pd.DataFrame()
df1['Location']=location
df1['Area'] = area
df1['BHK'] = BHK
df1['price'] = price

df1.to_csv("makan_data.csv",index=False)
 


# SCRAPPING DATA FROM HOMELINE.COM

from  selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as BS

url = "https://www.homeonline.com/property-for-rent-jaipur/?holsource=paid_search&holmedium=paid_google&gclid=Cj0KCQjwpcLZBRCnARIsAMPBgF3_eZtfDq2LZCtIRdzTXBjCLzrqicZAA09JR2CU8fx8Lx_2QWoUUfMaAjRREALw_wcB"
browser = webdriver.Firefox(executable_path=r"E:\geckodriver.exe")
browser.get(url)

def btn_click(browser_con):
    result = browser_con.find_element_by_xpath('/html/body/div[11]/div/div/div/div/div[2]/div[2]/div[2]/a')
    result.click()
    sleep(10)
    
    try:
      html_page = browser_con.page_source
    
    except Exception: 
    #  pass 
        html_page = browser_con.page_source
    return html_page

for i in range(0,42):
    page = btn_click(browser)

soup = BS(page,'lxml')



all_div = soup.find_all('div',class_ = "liststylecon")


#my_div = soup.find_all('div',{"id":"listContent"})
location=[]
area=[]
status=[]

l=[]
bath=[]
deposit=[]
furnished=[]
price = []
#location
for section in all_div:
    info = section.find_all('div',class_="proplisttext")
    for data in info:
        details = data.find_all('div',class_="propdetails")
        for i in details:
            loc = i.findAll('div',class_="col-sm-9")
            
            raw = loc[0].text.strip()
            n_raw = raw[:raw.find("View on Map")].strip()
            location.append(n_raw)
            
#bhk

bhk=[]
for section in all_div:
    info = section.find_all('div',class_="row propheading")
    for data in info:
        details = data.find_all('div',class_="col-sm-7 col-md-7")
        for i in details:
            b = i.find('h2')
            b = b.text.strip()
            if len(b)==0:
                bhk.append(int('1'))
            else:
                b=b[0]
                bhk.append(int(b))

#area
area=[]
for section in all_div:
    info = section.find_all('div',class_="proplisttext")
    for data in info:
        details = data.find_all('div',class_="propdetails")
        for i in details:
            loc = i.findAll('div',class_="col-sm-9")
            
            raw = loc[1].text.strip().split()
            raw = raw[0]
            l=[]
            for i in raw:
                if i.isdigit():
                    l.append(i)
                    
            s=''.join(l)
            if len(s) == 0:
                area.append(int('800'))
            else:    
                area.append(int(s))

#price
price=[]
for section in all_div:
    info = section.find_all('div',class_="proplisttext")
    for data in info:
        details = data.find_all('div',class_="row propheading")
        for i in details:
            loc = i.find('div',class_="pricesty")
            raw = loc.text.strip()
            raw = raw.replace(",","")
            raw = raw.split()
            if len(raw) == 3 and raw[1].lower() in ['lac','lacs','lakh','lakhs']:
                price.append(int(float(raw[0])*100000))
            else:
                price.append(int(float(raw[0])))
            
            
        
#Making the dataframe
import pandas as pd

df1 = pd.DataFrame()
df1['Location']=location
df1['Area'] = area
df1['BHK'] = bhk
df1['price'] = price
df1.to_csv("homeline_data.csv",index=False)




# SCRAPPING DATA FROM MAKAN.COM

import requests

# urls of the page 
url1='https://www.makaan.com/price-trends/property-rates-for-rent-in-jaipur'
url2='https://www.makaan.com/price-trends/property-rates-for-rent-in-jaipur?page=2'
url3='https://www.makaan.com/price-trends/property-rates-for-rent-in-jaipur?page=3'
url4='https://www.makaan.com/price-trends/property-rates-for-rent-in-jaipur?page=4'
url5='https://www.makaan.com/price-trends/property-rates-for-rent-in-jaipur?page=5'
url6='https://www.makaan.com/price-trends/property-rates-for-rent-in-jaipur?page=6'
url7='https://www.makaan.com/price-trends/property-rates-for-rent-in-jaipur?page=7'

#List of url of the pages
lst=[url1,url2,url3,url4,url5,url6,url7]

# Empty lists
locality=[]
bhk1=[]
bhk2=[]
bhk3=[]

# scrapping of the data from website
for url in lst:
    page=requests.get(url)
    from bs4 import BeautifulSoup
    pageData=BeautifulSoup(page.text)
    tbodiesDataLists=pageData.find_all('tbody')
    trDataList=tbodiesDataLists[0].find_all('tr')


    for i in trDataList:
        cells=i.find_all('td')
        locality.append(cells[0].text.strip())
        bhk1.append(cells[2].text.strip())
        bhk2.append(cells[4].text.strip())
        bhk3.append(cells[6].text.strip())


# converint the data into dataframe 
import pandas as pd
data=pd.DataFrame()
data["Locality"]=locality
data[1]= bhk1
data[2]=bhk2
data[3]=bhk3

# Filling Empty columns with 0
data[1]=data[1].replace('-','0')
data[2]=data[2].replace('-','0')
data[3]=data[3].replace('-','0')

# converting the sting values into float type
data[1] = [float(i.replace(',','') )for i in data[1]]
data[2] = [float(i.replace(',','') )for i in data[2]]
data[3] = [float(i.replace(',','') )for i in data[3]]


# Reshaping the Dataframe
data = pd.melt(data, id_vars=["Locality"],var_name="BHK", value_name="Price") 
data = data.sort_values(["BHK"])
#removing all zeros from the dataframe
data=data[(data!=0).all(axis=1)]
#resetting index    
data = data.reset_index(drop=True) 
data.to_csv('makan_data2.csv',index_col=0)


#  RESHAPING OF DATA


import pandas as pd
data=pd.read_csv('makan_data2.csv',index_col=0)
lst=[]
for i in data['BHK']:
    if i=='1 BHK':
        lst.append(1)
    elif i=='2 BHK':
        lst.append(2)
    else:
        lst.append(3)
data['BHK']=lst      

import random as rm 

lst1=[]
for i in range(56):
    lst1.append(rm.randrange(480,960))



lst2=[]
for i in range(81):
    lst2.append(rm.randrange(960,2020))


lst3=[]
for i in range(85):
    lst3.append(rm.randrange(1790,3040))

lst1.extend(lst2)
lst1.extend(lst3)

data2=pd.DataFrame()
data2['Locality']=data['Locality']
data2['Area_Sqft']=lst1
data2['BHK']=data['BHK']
data2['Price']=data['Price']


# rcreating a csv file
data2.to_csv('data2.csv')

import pandas as pd
data3=pd.read_csv('homeline_data.csv')
data3.columns=['Locality','Area_Sqft','BHK','Price']

data1=pd.read_csv('makan_data.csv')
data1.columns=['Locality','Area_Sqft','BHK','Price']


frames=[data1,data2,data3]
data=pd.concat(frames)

data['Area_Per_Sqft']=data['Price']/data['Area_Sqft']

#data=data.sort_values(["BHK"])
# FINAL CLEAN DATA
data.to_csv('project_data.csv')