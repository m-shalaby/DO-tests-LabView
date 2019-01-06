import pandas as pd
import os
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
            with open(filePath,'r') as f:
                if f.readline()=='LabVIEW Measurement\t\n':
                    skiprows = 22
                else:
                    skiprows = 0
            
            DOdata = pd.read_csv(filePath, skiprows=skiprows, delimiter='\t', header=None)
            DOdata.columns = ['time', 'Upstream DO', 'Downstream DO']
           
            timearrayU = []
            timearrayD = []
            UpDO = []
            DownDO = []

    
        
            timearrayU.append(DOdata.iat[0,0])
            timearrayD.append(DOdata.iat[0,0])
            UpDO.append(DOdata.iat[0,1])
            DownDO.append(DOdata.iat[0,2])
            
            i=0
            while i < DOdata.shape[0]-5:
            #for i in xrange(0,DOdata.shape[0]-5,2):  
                if abs(DOdata.iat[i,1] - DOdata.iat[i+2,1]) > 0.008:
                    timearrayU.append(DOdata.iat[i+3,0])
                    UpDO.append(DOdata.iat[i+3,1])
                    i = i+3
                else:
                    i =i+2
            
            i=0
            while i < DOdata.shape[0]-5:
            #for i in xrange(0,DOdata.shape[0]-5,2):  
                if abs(DOdata.iat[i,2] - DOdata.iat[i+2,2]) > 0.008:
                    timearrayU.append(DOdata.iat[i+3,0])
                    DownDO.append(DOdata.iat[i+3,2])
                    i = i+3
                else:
                    i =i+2
            
            #for i in xrange(0,DOdata.shape[0]-5,2):
             #   if abs(DOdata.iat[i,2] - DOdata.iat[i+2,2]) > 0.008:
              #      timearrayD.append(DOdata.iat[i+3,0])
               #     DownDO.append(DOdata.iat[i+3,2])
                #    i = i+3

            monot = [j-i for i, j in zip(UpDO[:-1], UpDO[1:])]
            monot2 = [i-j for i, j in zip(monot[:-1], monot[1:])]
            
            if any(i > 0.3 for i in monot):
                #pass
                if any(i < 0 for i in monot2):
             #   print(filePath)
            #if any(i <= -0.3 for i in monot):
                    print (filePath)

    

        except Exception as ex:
            print(str(ex))
            print(filePath)
            
            
            
print('Hello World!')
