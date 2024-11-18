# -*- coding: utf-8 -*-
"""Rapido.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Nlr88M4xT_Vu3RX9I-UpaEhVoBGNO6ZG
"""

#!unzip '/content/drive/MyDrive/ML_LUMINAR/archive (23).zip'

import numpy as np
import pandas as pd

df=pd.read_csv('/content/rides_data.csv')

"""UNDERSTANDING DATA"""

df.shape

df.dtypes

df

df.head(20)

df.tail(20)

df.info()

"""CLEANING"""

df.isna().sum()

df[df['ride_status']=='cancelled']

# Check for missing values
print(df.isnull().sum())

# Filling null values for canceled rides
df.loc[df['ride_status'] == 'cancelled', ['ride_charge', 'misc_charge', 'total_fare']] = 0
df.loc[df['ride_status'] == 'cancelled', 'payment_method'] = 'cancelled'

df.loc[df['ride_status'] == 'cancelled',['services']]

df.isnull().sum()

df.head(30)

df.duplicated().sum()

df.dtypes

"""Feature engineering"""

def cate(i):
  if i['ride_status']=='cancelled':
    return 'Cancelled'
  elif i['distance']<5:
    return 'Short'
  elif i['distance']>=5 and  i['distance']<=15:
    return 'Medium'
  else:
    return 'Long'

df['distance_category'] = df.apply(cate, axis=1)

df.head(5)

"""ANALYSIS"""

df.describe()

df[df['total_fare']==1048.800000] # parcel

df['ride_charge'].sum()

df['misc_charge'].sum()

"""outlier detection"""

obj=[]
num=[]
for i in df:
  if df[i].dtype == 'object':
    obj.append(i)
  else:
    num.append(i)

obj

num

import matplotlib.pyplot as plt
for i in num:
    plt.figure(figsize=(7,6))
    plt.boxplot(df[i])
    plt.title(f"Box Plot of {i}")
    plt.show()

#UNIVARIATE ANALYSIS:

for col in num:
  print(col)
  print('------------------------')
  print(f'Mean : {df[col].mean()}')
  print(f'Median : {df[col].median()}')
  print(f'Minimum of {col} : {df[col].min()}')
  print(f'Maximum of {col} : {df[col].max()}')
  print(f'Standard Deviation : {df[col].std()}')
  print(f'Variance : {df[col].var()}')
  print('********************************************')
  print()

# to draw hist plot of numerical columns graphically using for loop
for col in df:
  if df[col].dtype=="int" or df[col].dtype=='float':
    plt.figure(figsize=(6,4))   # figsize(width,height)
    plt.hist(df[col],bins=15)
    plt.title(f"Histplot of {col}")
    plt.yscale('log')
    plt.xlabel(f"{col}")
    plt.ylabel('Count')
    plt.show()

#Calculate the percentage of canceled rides versus completed rides for an overview of ride success.

ride_status_counts = df.groupby('ride_status').size()
ride_status_counts

ride_status_percentages = (ride_status_counts / len(df)) * 100 # returns a series

# percentages for canceled and completed rides
canceled_percentage = ride_status_percentages.get('cancelled', 0)# key and default
completed_percentage = ride_status_percentages.get('completed', 0)


print(f"Percentage of Canceled Rides: {canceled_percentage:.2f}%")
print(f"Percentage of Completed Rides: {completed_percentage:.2f}%")

ride_status_percentages = (ride_status_counts / len(df)) * 100
ride_status_percentages

# j=df['source'].value_counts().get('Balagere Harbor',0)
# j

#PIE PLOT OF SERVIECES

plt.pie(df['services'].value_counts(),labels=df['services'].value_counts().index,autopct="%1.0f%%")
plt.show()

plt.pie(df['payment_method'].value_counts(),labels=df['payment_method'].value_counts().index,autopct="%1.0f%%")
plt.show()

df['payment_method'].value_counts()

#hist plot of numerical colunms:
for col in df:
  if df[col].dtype=="int" or df[col].dtype=='float':
    plt.figure(figsize=(6,4))   # figsize(width,height)
    plt.hist(df[col],bins=10)
    plt.title(f"Histplot of {col}")
    plt.yscale('log') # chnaging to log scale for more visible clarity
    plt.xlabel(f"{col}")
    plt.ylabel('Count')
    plt.show()

for col in df:
  if df[col].dtype=="int" or df[col].dtype=='float':
    plt.figure(figsize=(6,4))   # figsize(width,height)
    plt.hist(df[col],bins=10)
    plt.title(f"Histplot of {col}")
    plt.xlabel(f"{col}")
    plt.ylabel('Count')
    plt.show()

# which hour is the most prefered:

df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S.%f')
df['hour'] = df['time'].dt.hour
df

import seaborn as sns
sns.countplot(x=df['hour'])
plt.xticks(rotation=45)
plt.yscale('log')
plt.show()

df['hour'].value_counts()

# to find which day is most prefered:

df['date'] = pd.to_datetime(df['date'])
df['day_name'] = df['date'].dt.day_name()

df

day_counts = df['day_name'].groupby(df['day_name']).count()

day_counts.sort_values(ascending=True)

#visualization
plt.bar(x=day_counts.index,height=day_counts)
plt.xticks(rotation=90)
plt.show()

plt.bar(x=day_counts.index,height=day_counts)
plt.xticks(rotation=90)
plt.yscale('log')
plt.show()

#Find the most common pickup and drop-off locations by counting occurrences of source and destination.

source_count = df['source'].groupby(df['source']).count()
source_count.sort_values(ascending=False).head(10)

source_count = df['destination'].groupby(df['destination']).count()
source_count.sort_values(ascending=False).head(10)

#  servies vs total fare

df[['services','total_fare']].groupby('services').agg(['count','mean','median','min','max','std'])

df[['services','duration']].groupby('services').agg(['count','mean','median','min','max','std'])

df[['services','distance']].groupby('services').agg(['count','mean','median','min','max','std'])

#total revenue in payment method

df[['payment_method','total_fare']].groupby('payment_method').agg(['sum','count','mean','median','min','max']).sort_values(by=('total_fare', 'count'), ascending=True)

#total revenue in distance category

df[['distance_category','total_fare']].groupby('distance_category').agg(['sum','count','mean','median','min','max']).sort_values(by=('total_fare', 'count'), ascending=False)

# Heatmap (correlation matrix):
var1=df.corr(numeric_only=True)
sns.heatmap(var1,annot=True)
plt.title('Heatmap')
plt.show()

#plots the mean of total_fare for each services
var2=df[['services','total_fare']].groupby('services').mean()
plt.plot(var2.index,var2)
plt.title('Services Vs total fare')
plt.xlabel('service')
plt.ylabel('mean of total fare')
plt.show()

df