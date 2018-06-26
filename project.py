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
LABEL=data2['Locality'].head(20)
LABELS=[str(i) for i in LABEL]
labels=d1.iloc[:,1].values
features=d1.iloc[:,0:1].values
features[:,0]=le.fit_transform(features[:,0])
lst=[int(i) for i in features]

import pylab as plt
plt.figure(figsize=(16,5))
plt.bar(lst, labels, align='center',color=['g','r','b','y','m'])
plt.xticks(lst, LABELS,rotation=80)
plt.title("Locality Vs Prices",fontsize=18)
plt.xlabel("Locality",fontsize=18)
plt.ylabel("Prices",fontsize=18)
plt.show()


#  PART 3 GRAPHICAL VIEWS FOR 1BHK , 2BHK AND 3BHK

import pandas as pd
data2 =pd.read_csv('data2.csv',index_col=0)
localities=data2['Locality']
bhk1=data2["1 BHK"]
bhk2=data2["2 BHK"]
bhk3=data2["3 BHK"]


# GRAPHICAL VIEW OF HOT AREAS FOR 1 BHK APARTMENTS


data_bhk=pd.DataFrame()
data_bhk['Localities']=localities
data_bhk['1 BHK']=bhk1
#removing all zeros from the dataframe
data_bhk=data_bhk[(data_bhk!=0).all(axis=1)]
#resetting index    
data_bhk = data_bhk.reset_index(drop=True) 

LABEL=data_bhk['Localities']
LABELS=[str(i) for i in LABEL]
l_bhk=data_bhk.iloc[:,1].values
f_bhk=data_bhk.iloc[:,0:1].values
f_bhk[:,0]=le.fit_transform(f_bhk[:,0])
lst=[int(i) for i in f_bhk]

import pylab as plt
plt.figure(figsize=(30,5))
plt.bar(lst, l_bhk, align='center',color=['g','r','b','y','m'])
plt.xticks(lst, LABELS,rotation=80)
plt.title("Locality Vs Prices",fontsize=18)
plt.xlabel("Locality",fontsize=18)
plt.ylabel("Prices",fontsize=18)
plt.show()



# GRAPHICAL VIEW OF HOT AREAS FOR 2 BHK APARTMENTS


data_bhk=pd.DataFrame()
data_bhk['Localities']=localities
data_bhk['1 BHK']=bhk2

#removing all zeros from the dataframe
data_bhk=data_bhk[(data_bhk!=0).all(axis=1)]

#resetting index    
data_bhk = data_bhk.reset_index(drop=True) 

LABEL=data_bhk['Localities']
LABELS=[str(i) for i in LABEL]
l_bhk=data_bhk.iloc[:,1].values
f_bhk=data_bhk.iloc[:,0:1].values
f_bhk[:,0]=le.fit_transform(f_bhk[:,0])
lst=[int(i) for i in f_bhk]

plt.figure(figsize=(30,5))
plt.bar(lst, l_bhk, align='center',color=['g','r','b','y','m'])
plt.xticks(lst, LABELS,rotation=80)
plt.title("Locality Vs Prices",fontsize=18)
plt.xlabel("Locality")
plt.ylabel("Prices",fontsize=18)
plt.show()


# GRAPHICAL VIEW OF HOT AREAS FOR 3 BHK APARTMENTS

data_bhk=pd.DataFrame()
data_bhk['Localities']=localities
data_bhk['1 BHK']=bhk3

#removing all zeros from the dataframe
data_bhk=data_bhk[(data_bhk!=0).all(axis=1)]

#resetting index    
data_bhk = data_bhk.reset_index(drop=True) 

LABEL=data_bhk['Localities']
LABELS=[str(i) for i in LABEL]
l_bhk=data_bhk.iloc[:,1].values
f_bhk=data_bhk.iloc[:,0:1].values
f_bhk[:,0]=le.fit_transform(f_bhk[:,0])
lst=[int(i) for i in f_bhk]

plt.figure(figsize=(30,5))
plt.bar(lst, l_bhk, align='center',color=['g','r','b','y','m'])
plt.xticks(lst, LABELS,rotation=80)
plt.title("Locality Vs Prices",fontsize=18)
plt.xlabel("Locality",fontsize=18)
plt.ylabel("Prices",fontsize=18)
plt.show()
