#!/usr/bin/env python3

import argparse
import pickle
import numpy as np
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
parser.add_argument('--fmcpico_range', type=str, help='FMC PICO range selection (only available for XBPMs)',
                    nargs='?', const='1 mA', default=None, choices=BPMEnums.FMCPICORANGE.keys())
parser.add_argument('--fmcpico_conv', action='store_true', help='FMC PICO conversion to engineering units',
                    default=False)
parser.add_argument('--bpm_list', type=str, help='Filename containing the device name of every BPMs to be read',
                    default='bpmlist.pickle')
parser.add_argument('--result_file', type=str, help='Filename where the current spectra matrix (Ncorrectors x Npoints) will be exported',
                    default='results.pickle')

args = parser.parse_args()


# Setup acquistiion parameters

with open(args.bpm_list, 'rb') as filehandle:
    # read the data as binary data stream
    bpmlist = pickle.load(filehandle)

nBPMs = len(bpmlist)
xy_read = np.zeros((2*nBPMs,args.nr_samples))  # initializing x and y arrays

iBPM = 0 # counter

for bpm_name in bpmlist:
    
    bpm = BPM(bpm_name, wait_for_connection=True)    
    bpm.nr_samples_pre = args.nr_samples
    bpm.nr_samples_post = args.nr_post_samples
    bpm.nr_shots = args.nr_shots
    bpm.acq_repeat = BPMEnums.ACQREPEAT[args.repetitive]
    bpm.acq_channel = BPMEnums.ACQCHAN[args.acq_channel]
    
    # Set range if present on command-line
    if args.fmcpico_range is not None:
        bpm.fmc_pico_range_ch0 = BPMEnums.FMCPICORANGE[args.fmcpico_range]
        bpm.fmc_pico_range_ch1 = BPMEnums.FMCPICORANGE[args.fmcpico_range]
        bpm.fmc_pico_range_ch2 = BPMEnums.FMCPICORANGE[args.fmcpico_range]
        bpm.fmc_pico_range_ch3 = BPMEnums.FMCPICORANGE[args.fmcpico_range]
    
    # Acquistion type
    bpm.acq_trigger = BPMEnums.ACQTRIGTYP[args.acq_trigger_type]
    # Acquistion type
    bpm.acq_event = BPMEnums.ACQEVENTS['Start']
    
    # Wait for acquisition to complete
    while not bpm.is_acq_completed:
        sleep(0.5)
    
    vals = {
        'X': {
            'data'  : np.array(bpm.array_x),
        },
        'Y': {
            'data'  : np.array(bpm.array_y),
        }
    }
    
    if args.fmcpico_conv:   

        # Conversion factor
        conv_factors = {
            BPMEnums.ACQCHAN['ADC']     : 524288,
            BPMEnums.ACQCHAN['ADCSwap'] : 524288,
            BPMEnums.ACQCHAN['TbT']     : 1048576,
            BPMEnums.ACQCHAN['FOFB']    : 5242880,
            BPMEnums.ACQCHAN['Monit1']  : 4096000
        }
        conv_factor = conv_factors.get(BPMEnums.ACQCHAN[bpm.acq_channel], 524288)
    
        for _, v in vals.items():
            range = v['range']
            v['data'] = (range/conv_factor) * v['data']
    
    # Store values
    
    xy_read[iBPM] = vals['X']['data']
    xy_read[nBPMs+iBPM] = vals['Y']['data']
    
    iBPM =+ 1

print('Fim da aquisição da matriz de dimensão', xy_read.shape, '\n e 10 primeiros valores da última linha \n', xy_read[-1][:10])
    
with open(args.result_file, 'wb') as filewrite:
    # store the data as binary data stream
    pickle.dump(xy_read, filewrite)    
    
'''
# Acquiring Response Matrix
ncor = 10
Rinv_x = Rinv_y = np.zeros((ncor,args.nr_samples))    


# Calculating kicks

kick_factor = 30e-6 # rad/A
theta = Rinv_x @ xy_read/kick_factor   

  '''  
