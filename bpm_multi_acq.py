#!/usr/bin/env python3

import argparse
import pickle
import numpy as np
import scipy.io
from time import sleep
from bpm.bpm import BPM, BPMEnums

parser = argparse.ArgumentParser(description='BPM Acquistion utility')
# parser.add_argument('prefix', type=str, help='EPICS PV prefix (e.g., SI-09SAFE:DI-PBPM-1:)')
parser.add_argument('nr_samples', type=int, help='Number of acquisition samples')
parser.add_argument('acq_channel', type=str, help='Acquisition channel',
                    choices=BPMEnums.ACQCHAN.keys())
parser.add_argument('--acq_trigger_type', type=str, help='Acquisition trigger type',
                    default='External', choices=BPMEnums.ACQTRIGTYP.keys())
parser.add_argument('--nr_post_samples', type=int, help='Number of acquisition post-trigger samples',
                    default=0)
parser.add_argument('--nr_shots', type=int, help='Number of acquisition shots',
                    default=1)
parser.add_argument('--repetitive', type=str, help='Repetitive acquisition',
                    default='Normal', choices=BPMEnums.ACQREPEAT.keys())
parser.add_argument('--bpm_list', type=str, help='Filename containing the device name of every BPMs to be read',
                    default='bpmlist.pickle')
parser.add_argument('-r','--result_file', type=str, help='Filename where the current spectra matrix (Ncorrectors x Npoints) will be exported',
                    default='results')

args = parser.parse_args()

ns = args.nr_samples

# Setup acquistiion parameters

with open(args.bpm_list, 'rb') as filehandle:
    # read the data as binary data stream
    bpmlist = pickle.load(filehandle)

nBPMs = len(bpmlist)
xy_read = np.zeros((2*nBPMs,args.nr_samples))  # initializing x and y array

iBPM = 0 # counter
bpm = {}

for bpm_name in bpmlist:
    print(bpm_name)
    bpm[bpm_name] = BPM(bpm_name, wait_for_connection=True)  
    
for k,v in bpm.items():
    v.nr_samples_pre = args.nr_samples
    v.nr_samples_post = args.nr_post_samples
    v.nr_shots = args.nr_shots
    v.acq_repeat = BPMEnums.ACQREPEAT[args.repetitive]
    v.acq_channel = BPMEnums.ACQCHAN[args.acq_channel]
    
    # Acquistion type
    v.acq_trigger = BPMEnums.ACQTRIGTYP[args.acq_trigger_type]
    # Acquistion type
    v.acq_event = BPMEnums.ACQEVENTS['Start']

for k,v in bpm.items():    
    # Wait for acquisition to complete
    while not v.is_acq_completed:
        sleep(0.5)
        print('Waiting for', k)
    
    vals = {
        'X': {
            'data'  : np.array(v.pos_x[:ns]),
        },
        'Y': {
            'data'  : np.array(v.pos_y[:ns]),
        }
    }
    print(vals['Y']['data'])
    # Store values
    
    xy_read[iBPM] = vals['X']['data']
    xy_read[nBPMs+iBPM] = vals['Y']['data']  # units in nm
    
    iBPM += 1

print('Fim da aquisição da matriz de dimensão', xy_read.shape, '\n e 10 primeiros valores da última linha \n', xy_read[-1][:10])
    
with open(args.result_file + '.pickle', 'wb') as filewrite:
    # store the data as binary data stream
    pickle.dump(xy_read, filewrite )    
    
scipy.io.savemat('./' + args.result_file + '.mat', mdict={'xy_read': xy_read})
