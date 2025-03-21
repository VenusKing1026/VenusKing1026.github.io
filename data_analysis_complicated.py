#!/usr/bin/env python
# coding: utf-8

# In[10]:


# %load data_analysis
#read data as raw_data
# select 2 question as data
# clean data
# do chi square test
# if there is relationshipo, change catagorical to numerical use dict
# do spearman;s test
# show plot

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import spearmanr
# read data
file_path='./HLFS Full Raw Data Set.csv'
raw_data=pd.read_csv(file_path)

# choose 
data=raw_data[['How often do you experience stress during the academic semester? ','On average, how many hours per day do you spend using a computer or other screens? ','Physical','ST for A','ST for E']]
data=data.rename(columns={'How often do you experience stress during the academic semester? ':'SF','On average, how many hours per day do you spend using a computer or other screens? ':'TST'})

#clean data
data=data.dropna()

data

dic={'Frequently':4,
        'Never':1,
        'Occasionally':3,
        'Rarely':2,
        'More than 6 hours':4,
        '4–6 hours':3,
        '1–3 hours':2,'Less than 1 hour':1}

# get physical activivy
data['Physical']=data['Physical'].str[0]

# change ST for A and E
data['ST for A']=data['ST for A'].map(dic)
data['ST for E']=data['ST for E'].map(dic)



# calculate Allocation
data['Allocation']=data['ST for A']/data['ST for E']


# psudocode:
# get physical activity
# get screentime for academic and entertaiment
# calculate allocation
# 
# group by physical activity
#
# in group, do chi_sqare and relational test
# in group, calculate allacation and stresslevel

# group by

HPEF=data[data['Physical'].isin(['C','D'])]
LPEF=data[data['Physical'].isin(['A','B'])]

def Chi(group):

    # chi square
    chi_table=pd.crosstab(group['SF'],group['TST'])
    # chi test check
    chi2, p, dof, expected = chi2_contingency(chi_table)

    print('Chi square table')
    print(chi_table)
    print(f"卡方统计量: {chi2}")
    print(f"p值: {p}")
    print(f"自由度: {dof}")
    print(f"期望频数:\n{expected}")

Chi(HPEF),Chi(LPEF)


# there is relationship, check its direction
#turn to numerical
LPEF['SF']=LPEF['SF'].map(dic)
LPEF['TST']=LPEF['TST'].map(dic)

# calculate spearman's coefficient

corr_low,p_low=spearmanr(LPEF['TST'],LPEF['SF'])


# there is relationship, check its direction
#turn to numerical
HPEF['SF']=HPEF['SF'].map(dic)
HPEF['TST']=HPEF['TST'].map(dic)


# calculate spearman's coefficient

corr_high,p_high=spearmanr(HPEF['TST'],HPEF['SF'])


# cofounding : allocation
r1,p1=spearmanr(HPEF['Allocation'],HPEF['SF'])
r2,p2=spearmanr(LPEF['Allocation'],LPEF['SF'])
rt,pt=spearmanr(data['Allocation'],data['SF'])
# print(r1,p1)
# print(r2,p2)
# print(rt,pt)


import pandas as pd
import numpy as np
from scipy.stats import spearmanr, norm


print(f"HPEF 组的斯皮尔曼相关系数: {corr_high}, p 值: {p_high}")
print(f"LPEF 组的斯皮尔曼相关系数: {corr_low}, p 值: {p_low}")

# Fisher's Z-transformation
def fisher_z(r):
    return np.arctanh(r)

# 计算 Z 值
z_high = fisher_z(corr_high)
z_low = fisher_z(corr_low)

# 计算 Z 差值
z_diff = z_high - z_low

# 计算标准误差
n_high = len(HPEF)
n_low = len(LPEF)
se = np.sqrt(1 / (n_high - 3) + 1 / (n_low - 3))

# 计算 Z 统计量
z_stat = z_diff / se

# 计算 p 值
p_value = 2 * (1 - norm.cdf(abs(z_stat)))

print(f"Z 差值: {z_diff}")
print(f"Z 统计量: {z_stat}")
print(f"p 值: {p_value}")




