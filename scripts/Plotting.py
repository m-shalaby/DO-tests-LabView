import csv
import os
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def fReader(path):
    
    df = pd.read_excel(path, sheetname=0, header = 0)
    
    return df

PressureMeans = fReader('/Users/m_ayman/Desktop/SURE/Data_Analysis/Pressure_means.xlsx')

#SamplePotMeans = fReader('C:\Users\Aaron\Desktop\McGill Means\SamplePot.xlsx')

#temp = SamplePotMeans[['deflector','wFlow','aContent','DO Difference']]
temp = PressureMeans[['deflector','wFlow','aContentNominal','P1-P2']]


temp['deflector']=temp['deflector'].astype(str)
#temp1 = temp.loc[temp['deflector'] == 3]
#temp = temp[temp.deflector.isin([3, 4, 5])]

#print('Hello World!')

for i in np.unique(temp.deflector):
    temp1 = temp.loc[temp['deflector'] == i]
    temp1.pivot(index='aContentNominal',columns='wFlow',values='P1-P2').plot(title = 'Deflector ' + i) #xlim = [0,10], ylim = [0,5])
    
    #print(i)

#print('Hello World!')



#temp.pivot(index='aContent',columns='wFlow',values='DO Difference').plot()

#InflowMeans = fReader('/Users/m_ayman/Desktop/SURE/Data_Analysis/Pressure_means.xlsx')



print('Hello World!')
