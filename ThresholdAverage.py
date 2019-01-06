import csv
import os
import pandas as pd
import seaborn as sns
import numpy as np

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

def Thresholder(x,a):
    #t = np.mean(x)
    #a = np.full((len(x),1), t)
    #t = t+a
    t = x>a
    t = x[t]
    t = np.mean(t)
    return t

def FlowAverage(x):
    m = np.mean(x)
    b = np.std(x)
    t = ((m-b) < x) & (x < (m+b))
    t = x[t]
    t = np.mean(t)
    
    #print('Hello World!')
    return t


def fAverage(path):
    with open(path,'r') as f:
        if f.readline()=='LabVIEW Measurement\t\n':
            skiprows = 22
        else:
            skiprows = 0
    df = pd.read_csv(path, skiprows=skiprows, nrows=99999, delimiter='\t', header=None)
    df.columns = ['time', 'aFlow', 'wPressure', 'aPressure', 'diffPressure']

    return df

data = pd.DataFrame(columns=['deflector', 'wFlow', 'atmPressure', 'temp', 'timestamp', 'wPressure', 'time', 'aPressure', 'aFlow','diffPressure', 'aFlowAvg','aPressureAvg','diffPressureAvg'])
for dirpath, dirnames, filenames in os.walk('/Users/m_ayman/Desktop/SURE/Data_Analysis'):
    for filename in [f for f in filenames if 'McGillP' in f]:
        filePath = os.path.join(dirpath, filename)
        tmp = [s0.split(' ') for s0 in splitall(dirpath) if 'Deflector ' in s0][0]
        deflector = tmp[1]      
        tmp = [s0 for s0 in filename.split('_') if s0!='']
        wFlow = tmp[1]
        atmPressure = tmp[2]
        temp = tmp[3]
        tmp = tmp[5]
        tmp = [s0 for s0 in tmp.split('.') if s0!='']
        timestamp = tmp[0]
        try:
            df = fAverage(filePath)
            df['deflector'] = pd.Series(deflector, index=df.index)
            df['wFlow'] = pd.Series(wFlow, index=df.index)
            df['temp'] = pd.Series(temp, index=df.index)
            df['timestamp'] = pd.Series(timestamp, index=df.index)
            df['atmPressure'] = pd.Series(atmPressure, index=df.index)
            
            tmp = df.wPressure
            df['wPressureAvg'] = Thresholder(tmp,0.001)
            
            tmp = df.aFlow
            df['aFlowAvg'] = FlowAverage(tmp)
            
            tmp = df.aPressure
            df['aPressureAvg'] = Thresholder(tmp,0.001)
            
            df['diffPressureAvg'] = pd.Series(df['diffPressure'].mean(), index=df.index)
            
            data = data.append(df)
        except Exception as ex:
            print(str(ex))
            print(filePath)            
            
            

tmp = data[['deflector','wPressureAvg','wFlow','timestamp','aFlowAvg','aPressureAvg','temp']]
            
means = tmp.groupby(['deflector', 'wFlow', 'timestamp' ], as_index=False).mean()


print('Hello World!') 
            

