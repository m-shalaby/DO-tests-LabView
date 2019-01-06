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

def aContentbin(x):
    a = np.array([0, 3, 5, 7, 10])
    d = abs(a-x)
    b = np.argmin(d)
    return a[b]

calibFunaPressure = lambda x: x*2012.985+-1.0097
calibFunaFlow = lambda x: x*0.5+0.006
calibFunwPressure = lambda x: x*2014.707+-1.06208

    
def fIF_P(path):
    with open(path,'r') as f:
        if f.readline()=='LabVIEW Measurement\t\n':
            skiprows = 22
        else:
            skiprows = 0
    DOdata = pd.read_csv(path, skiprows=skiprows, delimiter='\t', header=None)
    DOdata.columns = ['time', 'Upstream DO', 'Downstream DO', 'aFlow', 'wPressure', 'aPressure']
    
    
    timearrayU = []
    timearrayD = []
    UpDO = []
    DownDO = []
    
    a=0
    b=0
    
        
    timearrayU.append(DOdata.iat[0,0])
    timearrayD.append(DOdata.iat[0,0])
    UpDO.append(DOdata.iat[0,1])
    DownDO.append(DOdata.iat[0,2])
    
    for i in xrange(1,DOdata.shape[0]-100,100):
            
        if abs(DOdata.iat[i,1] - DOdata.iat[i+100,1]) > 0.01:
            timearrayU.append(DOdata.iat[i+100,0])
            UpDO.append(DOdata.iat[i+100,1])
        if abs(DOdata.iat[i,2] - DOdata.iat[i+100,2]) > 0.01:
            timearrayD.append(DOdata.iat[i+100,0])
            DownDO.append(DOdata.iat[i+100,2])
    if len(UpDO) == 1 or len(DownDO) == 1:
        print(path)
        a=UpDO[0]
        b=DownDO[0]
    elif len(UpDO) < len(DownDO):
        #a=UpDO[-1]
        #b=DownDO[-2]
        a=UpDO[1]
        b=DownDO[1]
    else:
        #b=DownDO[-1]
        #a=UpDO[-2]
        a=UpDO[1]
        b=DownDO[1]
    
    A1 = DOdata['aFlow']
    A1 = FlowAverage(A1)
    
    P1 = DOdata['wPressure']
    P1 = Thresholder(P1,0.001)
    
    P2 = DOdata['aPressure']
    P2 = Thresholder(P2,0.001)
    
    
    df = pd.DataFrame(columns = ['Upstream DO', 'Downstream DO', 'aFlowAvg', 'wPressureAvg', 'aPressureAvg'])
    
    df.set_value(0, 'Upstream DO', a)
    df.set_value(0, 'Downstream DO', b)
    df.set_value(0, 'aFlowAvg', A1)
    df.set_value(0, 'wPressureAvg', P1)
    df.set_value(0, 'aPressureAvg', P2)
    
    #print('Hello World!') 
    return df


data = pd.DataFrame(columns=['deflector', 'wFlow', 'atmPressure', 'temp', 'timestamp', 'aFlowAvg','aPressureAvg', 'aContent', 'aContentNominal'])
for dirpath, dirnames, filenames in os.walk('/Users/m_ayman/Desktop/SURE/Data_Analysis'):
    for filename in [f for f in filenames if 'McGillIF' in f]:
        filePath = os.path.join(dirpath, filename)
        tmp = [s0.split(' ') for s0 in splitall(dirpath) if 'Deflector ' in s0][0]
        deflector = tmp[1]      
        tmp = [s0 for s0 in filename.split('_') if s0!='']
        wFlow = tmp[1]
        '''if wFlow == '127,5':
            print(filePath)
    '''
        atmPressure = tmp[2]
        temp = tmp[3]
        tmp = tmp[5]
        tmp = [s0 for s0 in tmp.split('.') if s0!='']
        timestamp = tmp[0]
        try:
            df = fIF_P(filePath)
            df['deflector'] = pd.Series(deflector, index=df.index)
            df['wFlow'] = pd.Series(wFlow, index=df.index)
            df['temp'] = pd.Series(temp, index=df.index)
            df['timestamp'] = pd.Series(timestamp, index=df.index)
            df['atmPressure'] = pd.Series(atmPressure, index=df.index)







            data = data.append(df)
        except Exception as ex:
            print(str(ex))
            print(filePath)
            
 
 
 

data['aPressureAvg'] = data['aPressureAvg'].apply(calibFunaPressure)
data['wPressureAvg'] = data['wPressureAvg'].apply(calibFunwPressure)
data['aFlowAvg'] = data['aFlowAvg'].apply(calibFunaFlow)

data['wFlow'] = data['wFlow'].apply(float)
data['wFlow'] = data['wFlow']*0.0630902

data['aContent']= data['aFlowAvg']/data['wFlow']/(100+data['wPressureAvg'])*100*100
data['aContentNominal'] = data['aContent'].apply(aContentbin)
            
#print('Hello World!')
data.to_csv('/Users/m_ayman/Desktop/SURE/Data_Analysis/InFlow_P_firstupdate.csv')
