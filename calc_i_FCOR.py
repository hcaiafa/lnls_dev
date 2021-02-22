"""
Created on Mon Feb 15 19:29:56 2021

@author: henrique.caiafa
"""
import pickle
import numpy as np
import scipy.io
import matplotlib.pyplot as plt

acqfile = 'test100k.pickle'
with open('Rmat.pickle', 'rb') as filehandle:
    # read the data as binary data stream
    Rmat = pickle.load(filehandle)    # [um/urad]
    
U, s, V = np.linalg.svd(Rmat)

threshold = 1e-5

s_inv = np.array([1/i if i > threshold else 0. for i in s])

W_inv = np.zeros((len(V), len(U))) #, dtype=complex)

W_inv[:len(V), :len(V)] = np.diag(s_inv)

R_pseudoinv = np.linalg.multi_dot([V, W_inv, np.transpose(U)])

#R_pseudoinv = np.linalg.pinv(Rmat)

n_fcor, n_2bpm = R_pseudoinv.shape # dummy

fRF = 499.6649e6

fFOFB = fRF/19872
wFOFB = 2*np.pi*fFOFB

Ts = 1/fFOFB

# w_mains = 2.*np.pi*60;

with open(acqfile, 'rb') as filehandle2:
    # read the data as binary data stream
    xy_read = pickle.load(filehandle2)*1e-3    #converting units to um [MODIFY TO 1e-3!!!!!!!!!!!!]

_,ns = xy_read.shape

t = np.linspace(0.,ns*Ts,ns)

kick_factor = 0.03 # urad/mA
corr_signals = R_pseudoinv @ xy_read/kick_factor 

# plot correctors' time signals (largest std vs lowest std value)
corr_signals_std = np.std(corr_signals,axis=1)

min_index = np.argmin(corr_signals_std)
max_index = np.argmax(corr_signals_std)

plt.figure(1)
plt.plot(t,corr_signals[max_index],t,corr_signals[min_index])


freqs = np.fft.fftfreq(ns)*fFOFB

mask = freqs > 0  # list with indexes 

cur_spectra =  np.array( [ 2.0*np.abs(np.fft.fft(corr_signals[i])/ns) for i in range(n_fcor) ] )

# mean, max and min collumn-wise (i.e. for each fft bin)
cur_mean = np.mean(cur_spectra,axis=0)
#cur_max = np.max(cur_spectra,axis=0)
#cur_min = np.min(cur_spectra,axis=0)
cur_max = cur_spectra[max_index]
cur_min = cur_spectra[min_index]

'''
cur_mean =  np.array([ np.mean(cur_spectra[:,i]) for i in range(ns) ] )
cur_max =  np.array([ np.max(cur_spectra[:,i]) for i in range(ns) ] )
cur_min =  np.array([ np.min(cur_spectra[:,i]) for i in range(ns) ] )
'''

plt.figure(2)

plt.plot(freqs[mask],cur_max[mask],label="max std spectrum")
plt.plot(freqs[mask],cur_mean[mask],label="avg spectrum")
plt.plot(freqs[mask],cur_min[mask],label="min std spectrum")
plt.legend()
plt.yscale('log')
plt.ylabel('Amplitude [mA]')
plt.xlabel('Frequency [Hz]')
plt.grid(True)
plt.show()

