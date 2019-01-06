import csv
import os
import pandas as pd
import seaborn as sns
import numpy as np

#print("Hello World!")


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

def aContentbin(x):
    a = np.array([0, 3, 5, 7, 10])
    d = abs(a-x)
    b = np.argmin(d)
    return a[b]
    
def fAverage(path):
    with open(path,'r') as f:
        if f.readline()=='LabVIEW Measurement\t\n':
            skiprows = 22
        else:
            skiprows = 0
    df = pd.read_csv(path, skiprows=skiprows, nrows=99999, delimiter='\t', header=None)
    df.columns = ['time', 'aFlow', 'wPressure', 'aPressure', 'diffPressure']

    return df

calibFunaPressure = lambda x: x*2012.985+-1.0097
calibFunaFlow = lambda x: x*0.5+0.006
calibFunwPressure = lambda x: x*2014.707+-1.06208
calibFundiffPressure = lambda x: x*3448.836+-0.797


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
            
            tmp = df.wPressure
            #df['wPressureAvg'] = pd.Series(df['wPressure'].mean(), index=df.index)
            df['wPressureAvg'] = Thresholder(tmp,0.001)
            
            tmp = df.aFlow
            #df['aFlowAvg'] = pd.Series(df['aFlow'].mean(), index=df.index)
            df['aFlowAvg'] = FlowAverage(tmp)
            
            tmp = df.aPressure
            #df['aPressureAvg'] = pd.Series(df['aPressure'].mean(), index=df.index)
            df['aPressureAvg'] = Thresholder(tmp,0.001)
            
            df['diffPressureAvg'] = pd.Series(df['diffPressure'].mean(), index=df.index)
           
            
            data = data.append(df)
        except Exception as ex:
            print(str(ex))
            print(filePath)


data['aPressureAvg'] = data['aPressureAvg'].apply(calibFunaPressure)
data['aPressure'] = data['aPressure'].apply(calibFunaPressure)

data['wPressureAvg'] = data['wPressureAvg'].apply(calibFunwPressure)
data['wPressure'] = data['wPressure'].apply(calibFunwPressure)

data['aFlowAvg'] = data['aFlowAvg'].apply(calibFunaFlow)
data['aFlow'] = data['aFlow'].apply(calibFunaFlow)

tmp = data[['deflector','wPressureAvg','wFlow','timestamp','aFlowAvg','aPressureAvg','temp']]
            
means = tmp.groupby(['deflector', 'wFlow', 'timestamp' ], as_index=False).mean()

means['wFlow'] = means['wFlow'].apply(float)
means['wFlow'] = means['wFlow']*0.0630902

means['aContent']= means['aFlowAvg']/means['wFlow']/(100+means['wPressureAvg'])*100*100
means['aContentNominal'] = means['aContent'].apply(aContentbin)


means.to_csv('/Users/m_ayman/Desktop/SURE/Data_Analysis/Pressure_means.csv')
