"""
Created on Mon Feb 15 19:29:56 2021

@author: henrique.caiafa
"""
import pickle
import numpy as np
import scipy.io
import matplotlib.pyplot as plt


with open('Rmat.pickle', 'rb') as filehandle:
    # read the data as binary data stream
    Rmat = pickle.load(filehandle)    
    
#U, W, V = np.linalg.svd(Rmat)

R_pseudoinv = np.linalg.pinv(Rmat)

n_fcor, n_2bpm = R_pseudoinv.shape # dummy

fRF = 499.6649e6

fFOFB = fRF/19872
wFOFB = 2*np.pi*fFOFB

Ts = 1/fFOFB

## Dummy code
ns =int(1e4)
t = np.linspace(0.,ns*Ts,ns)

w_mains = 2.*np.pi*60;

xy_read = np.array( [np.random.rand()*(np.cos(w_mains*t)+0.5*np.cos(2*w_mains*t)) for i in range(n_2bpm)]  ) 

plt.figure(1)
plt.plot(t,xy_read[0],t,xy_read[1])

kick_factor = 30 # urad/A
corr_signals = R_pseudoinv @ xy_read/kick_factor 

freqs = np.fft.fftfreq(ns)*fFOFB

mask = freqs > 0  # list with indexes 

cur_spectra =  np.array( [ 2.0*np.abs(np.fft.fft(corr_signals[i])/ns) for i in range(n_fcor) ] )

cur_mean =  np.array([ np.mean(cur_spectra[:,i]) for i in range(ns) ] )
cur_max =  np.array([ np.max(cur_spectra[:,i]) for i in range(ns) ] )
cur_min =  np.array([ np.min(cur_spectra[:,i]) for i in range(ns) ] )

plt.figure(2)

plt.plot(freqs[mask],cur_mean[mask],freqs[mask],cur_max[mask],freqs[mask],cur_min[mask])

plt.show()

