# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 19:29:56 2021

@author: henrique.caiafa
"""
import pickle

'''
BPM list of sector 01
bpmlist = [
'SI-01M1:DI-BPM:PosX-Mon',
'SI-01M2:DI-BPM:PosX-Mon',
'SI-01C1:DI-BPM-1:PosX-Mon',
'SI-01C1:DI-BPM-2:PosX-Mon',
'SI-01C2:DI-BPM:PosX-Mon',
'SI-01C3:DI-BPM-1:PosX-Mon',
'SI-01C3:DI-BPM-2:PosX-Mon',
'SI-01C4:DI-BPM:PosX-Mon'
]
'''
nsec = 20

bpmlist = []

for isec in range(20):
    ilist = [
    'SI-'+str(isec+1).zfill(2)+'M1:DI-BPM:PosX-Mon',
    'SI-'+str(isec+1).zfill(2)+'M2:DI-BPM:PosX-Mon',
    'SI-'+str(isec+1).zfill(2)+'C1:DI-BPM-1:PosX-Mon',
    'SI-'+str(isec+1).zfill(2)+'C1:DI-BPM-2:PosX-Mon',
    'SI-'+str(isec+1).zfill(2)+'C2:DI-BPM:PosX-Mon',
    'SI-'+str(isec+1).zfill(2)+'C3:DI-BPM-1:PosX-Mon',
    'SI-'+str(isec+1).zfill(2)+'C3:DI-BPM-2:PosX-Mon',
    'SI-'+str(isec+1).zfill(2)+'C4:DI-BPM:PosX-Mon'
    ]
    bpmlist.extend(ilist)


with open('bpmlist.pickle', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(bpmlist, filehandle)

with open('bpmlist.pickle', 'rb') as filehandle:
    # read the data as binary data stream
    bpmlist2 = pickle.load(filehandle)    
    
print(bpmlist2)