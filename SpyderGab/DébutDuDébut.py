#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 15:31:37 2020

@author: Gabriel
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Loading Dataset
data = pd.read_csv('customers.csv')

# Cleaning Dataset to keep only active loyal members
data_cleaned = data[data['Churn']=='Yes']

# See teh distribution of the tenure
data_cleaned['tenure'].hist(bins=15)
plt.title("Histogram of tenure")
plt.xlabel('tenure')
plt.ylabel('Sum of clients')


# Binning the data per loyalty 
bins = np.array([0,10,45,data_cleaned['tenure'].max()])
group_names = ['New', 'Loyal', 'Very Loyal']
labels = pd.cut(data_cleaned['tenure'], bins, labels=group_names)

# Grouping the data by labels and gender <---> you may want to change that 
grouped = data_cleaned.groupby([labels,'gender'])
Gender_loyalty = grouped.size().unstack()

Gender_loyalty.plot.barh(title='Loyalty by gender')
# From this plot one can observe the distribution of clients within the loyalty classification made above 

# Getting all the services into one plot 
# Normalize the services for their binary value 
# Setting bool to int
My_dict={'Yes':1,'No':0}
data_cleaned['PhoneService_int']=data_cleaned['PhoneService'].map(My_dict)

grouped2 = data_cleaned.groupby(labels)
PhoneService_norm = grouped2['PhoneService_int'].sum()/grouped2.size()
normed_infos = pd.DataFrame(PhoneService_norm,columns=['Has_PhoneService'])



# Getting the proportion on people with internet service

My_dict2={'DSL':1,'Fiber optic':1,'No':0}
data_cleaned['InternetService_int']=data_cleaned['InternetService'].map(My_dict2)

InternetService_norm = grouped2['InternetService_int'].sum()/grouped2.size()
normed_infos['Has_InternetService'] = InternetService_norm


props = {
    'title': 'Percent of clients who have different services per loyalty',
    'ylabel': 'Normalized "Yes"'
}


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set(**props)
ax.legend(loc='best')
normed_infos.plot.bar(ax=ax,rot=30)

# Analyze the internet services
data_cleaned_with_internet = data_cleaned[data_cleaned['InternetService']!= 'No']
labels2 = pd.cut(data_cleaned_with_internet['tenure'], bins, labels=group_names)
grouped3 = data_cleaned_with_internet.groupby(labels2)

internet_services_df = normed_infos.copy()

for x in data_cleaned.columns[9:15]:
    new_col = x + '_int'
    data_cleaned_with_internet[new_col]=data_cleaned_with_internet[x].map(My_dict)
    
    current_norm = grouped3[new_col].sum()/grouped3.size()
    internet_services_df['Has_'+x] = current_norm
    

internet_services_df.drop(columns=['Has_InternetService','Has_PhoneService'],inplace=True)

props2 = {
    'title': 'Percent of clients who have different internet services per loyalty',
    'ylabel': 'Normalized "Yes"'
}


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set(**props)
ax.legend(loc='best')
internet_services_df.plot.bar(ax=ax,rot=30)

# money spent per loyalty

data_cleaned['Labels']=labels
fig = plt.figure()
sns.barplot(x='Labels', y='MonthlyCharges',data=data_cleaned)
sns.set(style="whitegrid")

# Do women spend more money ?

fig = plt.figure()
sns.catplot(x='Labels', y='MonthlyCharges',hue='gender',data=data_cleaned)
sns.set(style="whitegrid")

# Other representation 

fig = plt.figure()
sns.catplot(x='Labels', y='MonthlyCharges', hue='gender',kind="bar",data=data_cleaned)
sns.set(style="whitegrid")







