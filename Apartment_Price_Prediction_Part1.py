# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 23:39:45 2018

@author: Bantee Rathor
"""


import pandas as pd

data=pd.read_csv('project_data.csv',index_col=0)

features=data.iloc[:,0:-1].values
labels=data.iloc[:,-1:].values

from sklearn.preprocessing import LabelEncoder,OneHotEncoder
le=LabelEncoder()
features[:,0]=le.fit_transform(features[:,0])

onhler=OneHotEncoder(categorical_features=[0])
features=onhler.fit_transform(features).toarray()
features=features[:,1:]

# features scalling
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
features=sc.fit_transform(features)

# splitting of data for training and testing 
from sklearn.model_selection import train_test_split as TTS
features_train,features_test,labels_train,labels_test=TTS(features,labels,test_size=0.3,random_state=0)

# Fitting the model
from sklearn.ensemble import RandomForestRegressor
regressor=RandomForestRegressor(n_estimators=10,random_state=0)
regressor.fit(features,labels)

#predicting the test results
labels_pred=regressor.predict(features_test)

#model score
Score=regressor.score(features_test,labels_test)




# PART 2 TO FIND OUT HOT AREAS FOR APARTMENTS
data2=data.Area_Per_Sqft.groupby(data.Locality.str.title()).mean().reset_index().sort_values('Area_Per_Sqft',ascending=False).reset_index()


data2=data2.head(20)
hot_locations=data2['Locality'].head(20)
hot_locations=[str(i) for i in hot_locations]

area_per_sqft=data2.iloc[:,2].values
locations=data2.iloc[:,1:2].values
locations[:,0]=le.fit_transform(locations[:,0])
lst=[int(i) for i in locations]

import pylab as plt
plt.figure(figsize=(26,5))
plt.bar(lst, area_per_sqft, align='center',color=['g','r','b','y','m'])
plt.xticks(lst, hot_locations,rotation=80)
plt.title("Locality Vs Area/sqft",fontsize=18)
plt.xlabel("Locality",fontsize=18)
plt.ylabel("Area/sqft",fontsize=18)
plt.show()


# GRAPHICAL VIEW OF HOT AREAS FOR 1 BHK APARTMENTS

bhk1=data[data['BHK']==1]
bhk1=bhk1.Area_Per_Sqft.groupby(bhk1.Locality.str.title()).mean().reset_index().sort_values('Area_Per_Sqft',ascending=False).reset_index()
bhk1=bhk1.head(20)
# Separate locality
hot_locations=bhk1['Locality'].head(20)
hot_locations=[str(i) for i in hot_locations]#convert object to string

area_per_sqft=bhk1.iloc[:,-1].values# Labels to  plot
locations=bhk1.iloc[:,0:1].values# Features to plot
locations[:,0]=le.fit_transform(locations[:,0])#label encoding
lst=[int(i) for i in locations]# To convert strings into integer values

import pylab as plt
plt.figure(figsize=(26,5))
plt.bar(lst, area_per_sqft, align='center',color=['g','r','b','y','m'])
plt.xticks(lst, hot_locations,rotation=80)
plt.title("Locality Vs Area/sqft",fontsize=18)
plt.xlabel("Locality",fontsize=18)
plt.ylabel("Area/sqft",fontsize=18)
plt.show()




# GRAPHICAL VIEW OF HOT AREAS FOR 2 BHK APARTMENTS


bhk2=data[data['BHK']==2]
bhk2=bhk2.Area_Per_Sqft.groupby(bhk2.Locality.str.title()).mean().reset_index().sort_values('Area_Per_Sqft',ascending=False).reset_index()
bhk2=bhk2.head(20)
# Separate locality
hot_locations=bhk2['Locality'].head(20)
hot_locations=[str(i) for i in hot_locations]#convert object to string

area_per_sqft=bhk2.iloc[:,-1].values# Labels to  plot
locations=bhk2.iloc[:,0:1].values# Features to plot
locations[:,0]=le.fit_transform(locations[:,0])#label encoding
lst=[int(i) for i in locations]# To convert strings into integer values

import pylab as plt
plt.figure(figsize=(26,5))
plt.bar(lst, area_per_sqft, align='center',color=['g','r','b','y','m'])
plt.xticks(lst, hot_locations,rotation=80)
plt.title("Locality Vs Area/sqft",fontsize=18)
plt.xlabel("Locality",fontsize=18)
plt.ylabel("Area/sqft",fontsize=18)
plt.show()



# GRAPHICAL VIEW OF HOT AREAS FOR 3 BHK APARTMENTS


bhk3=data[data['BHK']==3]
bhk3=bhk3.Area_Per_Sqft.groupby(bhk3.Locality.str.title()).mean().reset_index().sort_values('Area_Per_Sqft',ascending=False).reset_index()
bhk3=bhk3.head(20)
# Separate locality
hot_locations=bhk3['Locality'].head(20)
hot_locations=[str(i) for i in hot_locations]#convert object to string

area_per_sqft=bhk3.iloc[:,-1].values# Labels to  plot
locations=bhk3.iloc[:,0:1].values# Features to plot
locations[:,0]=le.fit_transform(locations[:,0])#label encoding
lst=[int(i) for i in locations]# To convert strings into integer values

import pylab as plt
plt.figure(figsize=(26,5))
plt.bar(lst, area_per_sqft, align='center',color=['g','r','b','y','m'])
plt.xticks(lst, hot_locations,rotation=80)
plt.title("Locality Vs Area/sqft",fontsize=18)
plt.xlabel("Locality",fontsize=18)
plt.ylabel("Area/sqft",fontsize=18)
plt.show()
