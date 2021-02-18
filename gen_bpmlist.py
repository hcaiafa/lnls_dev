# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 19:29:56 2021

@author: henrique.caiafa
"""
import pickle

'''
BPM list of sector 01
bpmlist = [
'SI-01M1:DI-BPM:',
'SI-01M2:DI-BPM:',
'SI-01C1:DI-BPM-1:',
'SI-01C1:DI-BPM-2:',
'SI-01C2:DI-BPM:',
'SI-01C3:DI-BPM-1:',
'SI-01C3:DI-BPM-2:',
'SI-01C4:DI-BPM:'
]
'''
nsec = 20

bpmlist = []

for isec in range(nsec):
    ilist = [
    'SI-'+str(isec+1).zfill(2)+'M1:DI-BPM:',
    'SI-'+str(isec+1).zfill(2)+'M2:DI-BPM:',
    'SI-'+str(isec+1).zfill(2)+'C1:DI-BPM-1:',
    'SI-'+str(isec+1).zfill(2)+'C1:DI-BPM-2:',
    'SI-'+str(isec+1).zfill(2)+'C2:DI-BPM:',
    'SI-'+str(isec+1).zfill(2)+'C3:DI-BPM-1:',
    'SI-'+str(isec+1).zfill(2)+'C3:DI-BPM-2:',
    'SI-'+str(isec+1).zfill(2)+'C4:DI-BPM:'
    ]
    bpmlist.extend(ilist)


with open('bpmlist.pickle', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(bpmlist, filehandle)

with open('bpmlist.pickle', 'rb') as filehandle:
    # read the data as binary data stream
    bpmlist2 = pickle.load(filehandle)    
    
print(bpmlist2[-1])
