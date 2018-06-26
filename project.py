# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 00:37:46 2018

@author: Bantee Rathor
"""





import requests
import numpy as np

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
data["1 BHK"]= bhk1
data["2 BHK"]=bhk2
data["3 BHK"]=bhk3

# Filling Empty columns with 0
data["1 BHK"]=data["1 BHK"].replace('-','0')
data["2 BHK"]=data["2 BHK"].replace('-','0')
data["3 BHK"]=data["3 BHK"].replace('-','0')

# converting the sting values into float type
data["1 BHK"] = [float(i.replace(',','') )for i in data["1 BHK"]]
data["2 BHK"] = [float(i.replace(',','') )for i in data["2 BHK"]]
data["3 BHK"] = [float(i.replace(',','') )for i in data["3 BHK"]]


data2=data.to_csv('data2.csv')

# Reshaping the Dataframe
data = pd.melt(data, id_vars=["Locality"],var_name="BHK", value_name="Price") 
data = data.sort_values(["Locality",'Price'])
       
#removing all zeros from the dataframe
data=data[(data!=0).all(axis=1)]

#resetting index    
data = data.reset_index(drop=True) 

'''# creating csv file
data.to_csv('data.csv')

import pandas as pd
data=pd.read_csv('data.csv',index_col=0)
data=data.sort_values(['Locality'],ascending=True)'''

features=data.iloc[:,0:-1].values
labels=data.iloc[:,-1:].values

from sklearn.preprocessing import LabelEncoder,OneHotEncoder
le=LabelEncoder()
features[:,0]=le.fit_transform(features[:,0])
features[:,1]=le.fit_transform(features[:,1])

onhler=OneHotEncoder(categorical_features=[0])
features=onhler.fit_transform(features).toarray()
features=features[:,1:]

# features scalling
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
features=sc.fit_transform(features)

from sklearn.model_selection import train_test_split as TTS
features_train,features_test,labels_train,labels_test=TTS(features,labels,test_size=0.3,random_state=0)

from sklearn.ensemble import RandomForestRegressor
regressor=RandomForestRegressor(n_estimators=10,random_state=0)
regressor.fit(features,labels)

#predicting the test results
labels_pred=regressor.predict(features_test)

#model score
score=regressor.score(features_test,labels_test)



# PART 2 TO FIND OUT HOT AREAS FOR APARTMENTS

data2=data.Price.groupby(data.Locality.str.title()).sum().reset_index().sort_values('Price',ascending=False)
d1=data2.head(20)
labels2=d1.iloc[:,1:2].values
features2=d1.iloc[:,0:1].values

#features2[:,0]=le.fit_transform(features2[:,0])
import matplotlib.pyplot as plt
plt.figure(figsize=(25,5))
plt.scatter(features2,labels2,color='red')
plt.plot(features2,labels2,color='blue')
plt.title("Locality Vs Prices")
plt.xlabel("Locality")
plt.ylabel("Prices")
plt.show()


#  PART 3 GRAPHICAL VIEWS FOR 1BHK , 2BHK AND 3BHK

import pandas as pd
data2 =pd.read_csv('data2.csv',index_col=0)
localities=data2['Locality']
bhk1=data2["1 BHK"]
bhk2=data2["2 BHK"]
bhk3=data2["3 BHK"]


# GRAPHICAL VIEW OF HOT AREAS FOR 1 BHK APARTMENTS

data_1bhk=pd.DataFrame()
data_1bhk['Localities']=localities
data_1bhk['1 BHK']=bhk1
#removing all zeros from the dataframe
data_1bhk=data_1bhk[(data_1bhk!=0).all(axis=1)]
#resetting index    
data_1bhk = data_1bhk.reset_index(drop=True) 

d1bhk=data_1bhk.head(20)
l_1bhk=d1bhk.iloc[:,1:2].values
f_1bhk=d1bhk.iloc[:,0:1].values
#features2[:,0]=le.fit_transform(features2[:,0])

import matplotlib.pyplot as plt
plt.figure(figsize=(30,5))
plt.scatter(f_1bhk,l_1bhk,color='red')
plt.plot(f_1bhk,l_1bhk,color='blue')
plt.title("Locality Vs  1 BHK Prices")
plt.xlabel("Locality")
plt.ylabel("1 BHK Prices")
plt.show()


# GRAPHICAL VIEW OF HOT AREAS FOR 2 BHK APARTMENTS

data_2bhk=pd.DataFrame()
data_2bhk['Localities']=localities
data_2bhk['2 BHK']=bhk2
#removing all zeros from the dataframe
data_2bhk=data_2bhk[(data_2bhk!=0).all(axis=1)]
#resetting index    
data_2bhk = data_2bhk.reset_index(drop=True) 

d2bhk=data_2bhk.head(20)
l_2bhk=d2bhk.iloc[:,1:2].values
f_2bhk=d2bhk.iloc[:,0:1].values
#features2[:,0]=le.fit_transform(features2[:,0])

import matplotlib.pyplot as plt
plt.figure(figsize=(30,5))
plt.scatter(f_2bhk,l_2bhk,color='red')
plt.plot(f_2bhk,l_2bhk,color='blue')
plt.title("Locality Vs  1 BHK Prices")
plt.xlabel("Locality")
plt.ylabel("1 BHK Prices")
plt.show()


# GRAPHICAL VIEW OF HOT AREAS FOR 3 BHK APARTMENTS

data_3bhk=pd.DataFrame()
data_3bhk['Localities']=localities
data_3bhk['3 BHK']=bhk3
#removing all zeros from the dataframe
data_3bhk=data_3bhk[(data_3bhk!=0).all(axis=1)]
#resetting index    
data_3bhk = data_3bhk.reset_index(drop=True) 

d3bhk=data_3bhk.head(20)
l_3bhk=d3bhk.iloc[:,1:2].values
f_3bhk=d3bhk.iloc[:,0:1].values
#features2[:,0]=le.fit_transform(features2[:,0])

import matplotlib.pyplot as plt
plt.figure(figsize=(30,5))
plt.scatter(f_3bhk,l_3bhk,color='red')
plt.plot(f_3bhk,l_3bhk,color='blue')
plt.title("Locality Vs  1 BHK Prices")
plt.xlabel("Locality")
plt.ylabel("1 BHK Prices")
plt.show()




