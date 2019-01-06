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

t = 175.5

def flinReg(x,t1,DO1):
           
    for i in range(0,len(t1)-1):
        if x>t1[i]:
            if x<t1[i+1]:
                break
    
    val = (DO1[i+1]-DO1[i])/(t1[i+1]-t1[i])*(x-t1[i])+DO1[i]
    #print('Hello World!')
    return val





def fSPDO(path):
    with open(path,'r') as f:
#        if f.readline()=='LabVIEW Measurement\t\n':
        skiprows = 22
#        else:
#            skiprows = 0
            
        DOdata = pd.read_csv(path, skiprows=skiprows, delimiter='\t', header=None)
        DOdata.columns = ['time', 'Upstream DO', 'Downstream DO']
        
    timearrayU = []
    timearrayD = []
    UpDO = []
    DownDO = []
    
        
    timearrayU.append(DOdata.iat[0,0])
    timearrayD.append(DOdata.iat[0,0])
    UpDO.append(DOdata.iat[0,1])
    DownDO.append(DOdata.iat[0,2])
    
    
    
    for i in range(0,DOdata.shape[0]-2):       
        if abs(DOdata.iat[i,1] - DOdata.iat[i+1,1]) > 0.008:
            timearrayU.append(DOdata.iat[i+2,0])
            UpDO.append(DOdata.iat[i+2,1])
        if abs(DOdata.iat[i,2] - DOdata.iat[i+1,2]) > 0.008:
            timearrayD.append(DOdata.iat[i+2,0])
            DownDO.append(DOdata.iat[i+2,2])
            
    timearrayU.append(DOdata.iat[-1,0])
    timearrayD.append(DOdata.iat[-1,0])
    UpDO.append(DOdata.iat[-1,1])
    DownDO.append(DOdata.iat[-1,2])
    
    df = pd.DataFrame(columns = ['Upstream DO', 'Downstream DO'])
    
    
    
    a = flinReg(t,timearrayU,UpDO)
    b = flinReg(t,timearrayD,DownDO)
    
    
    df.set_value(0, 'Upstream DO', a)
    df.set_value(0, 'Downstream DO', b)   

    return df


data = pd.DataFrame(columns=['deflector', 'wFlow', 'atmPressure', 'temp', 'timestamp', 'aContentNominal', 'Upstream DO', 'Downstream DO'])
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
            df['aContentNominal'] = pd.Series(aContent, index=df.index)
            df['atmPressure'] = pd.Series(atmPressure, index=df.index)
            
            
            data = data.append(df)
        except Exception as ex:
            print(str(ex))
            print(filePath)



#print('Hello WORLD!')
data.to_csv('/Users/m_ayman/Desktop/SURE/Data_Analysis/SamplePot_linREG.csv')



















