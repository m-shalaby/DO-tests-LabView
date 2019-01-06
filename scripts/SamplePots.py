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


def fSPDO(path):
    with open(path,'r') as f:
        if f.readline()=='LabVIEW Measurement\t\n':
            skiprows = 22
        else:
            skiprows = 0
            
        DOdata = pd.read_csv(path, skiprows=skiprows, delimiter='\t', header=None)
        DOdata.columns = ['time', 'Upstream DO', 'Downstream DO']
        
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
    
    for i in range(1,DOdata.shape[0]-1):
            
        if abs(DOdata.iat[i,1] - DOdata.iat[i+1,1]) > 0.01:
            timearrayU.append(DOdata.iat[i+1,0])
            UpDO.append(DOdata.iat[i+1,1])
        if abs(DOdata.iat[i,2] - DOdata.iat[i+1,2]) > 0.01:
            timearrayD.append(DOdata.iat[i+1,0])
            DownDO.append(DOdata.iat[i+1,2])
    if len(UpDO) < len(DownDO):
        a=UpDO[-1]
        b=DownDO[-2]
    else:
        b=DownDO[-1]
        a=UpDO[-2]
    
    df = pd.DataFrame(columns = ['Upstream DO', 'Downstream DO'])
    
    df.set_value(0, 'Upstream DO', a)
    df.set_value(0, 'Downstream DO', b)   

    return df


data = pd.DataFrame(columns=['deflector', 'wFlow', 'atmPressure', 'temp', 'timestamp', 'aContent', 'Upstream DO', 'Downstream DO'])
for dirpath, dirnames, filenames in os.walk('/Users/m_ayman/Desktop/SURE/Data_Analysis'):
    for filename in [f for f in filenames if 'McGillSP' in f]:
        filePath = os.path.join(dirpath, filename)
        tmp = [s0.split(' ') for s0 in splitall(dirpath) if 'Deflector ' in s0][0]
        deflector = tmp[1]      
        tmp = [s0 for s0 in filename.split('_') if s0!='']
        wFlow = tmp[1]
        aContent = tmp[2]
        atmPressure = tmp[3]
        temp = tmp[4]
        tmp = tmp[5]
        tmp = [s0 for s0 in tmp.split('.') if s0!='']
        timestamp = tmp[0]
        try:
            
            df = fSPDO(filePath)
            df['deflector'] = pd.Series(deflector, index=df.index)
            df['wFlow'] = pd.Series(wFlow, index=df.index)
            df['temp'] = pd.Series(temp, index=df.index)
            df['timestamp'] = pd.Series(timestamp, index=df.index)
            df['aContent'] = pd.Series(aContent, index=df.index)
            df['atmPressure'] = pd.Series(atmPressure, index=df.index)
            
            
            data = data.append(df)
        except Exception as ex:
            print(str(ex))
            print(filePath)



data.to_csv('/Users/m_ayman/Desktop/SURE/Data_Analysis/SamplePot.csv')



















