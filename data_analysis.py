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


file_path='../HLFS Full Raw Data Set.csv'
raw_data=pd.read_csv(file_path)

data=raw_data[['How often do you experience stress during the academic semester? ','On average, how many hours per day do you spend using a computer or other screens? ']]
data=data.rename(columns={'How often do you experience stress during the academic semester? ':'SF','On average, how many hours per day do you spend using a computer or other screens? ':'TST'})


#print(data[pd.isnull(data.SF)])
data=data.dropna()
print(data[pd.isnull(data.SF)])

# chi square
chi_table=pd.crosstab(data['SF'],data['TST'])
print('Chi square table')
print(chi_table)

from scipy.stats import chi2_contingency

# chi test check
chi2, p, dof, expected = chi2_contingency(chi_table)

print(f"卡方统计量: {chi2}")
print(f"p值: {p}")
print(f"自由度: {dof}")
print(f"期望频数:\n{expected}")

# there is relationship, check its direction
dic={'Frequently':3,
        'Never':0,
        'Occasionally':2,
        'Rarely':1,
        'More than 6 hours':3,
        '4–6 hours':2,
        '1–3 hours':1,'Less than 1 hour':0  }



data['SF']=data['SF'].map(dic)
data['TST']=data['TST'].map(dic)

# calculate spearman's coefficient

r=data['SF'].corr(data['TST'],method='spearman')
print(r)