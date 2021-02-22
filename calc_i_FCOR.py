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

s_inv = np.array([1/i for i in s if i > 1e-5])

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

plt.figure(1)
plt.plot(t,xy_read[0],t,xy_read[1])

kick_factor = 0.03 # urad/mA
corr_signals = R_pseudoinv @ xy_read/kick_factor 

freqs = np.fft.fftfreq(ns)*fFOFB

mask = freqs > 0  # list with indexes 

cur_spectra =  np.array( [ 2.0*np.abs(np.fft.fft(corr_signals[i])/ns) for i in range(n_fcor) ] )

cur_mean =  np.array([ np.mean(cur_spectra[:,i]) for i in range(ns) ] )
cur_max =  np.array([ np.max(cur_spectra[:,i]) for i in range(ns) ] )
cur_min =  np.array([ np.min(cur_spectra[:,i]) for i in range(ns) ] )

plt.figure(2)

plt.plot(freqs[mask],cur_max[mask],label="max spectrum")
plt.plot(freqs[mask],cur_mean[mask],label="avg spectrum")
plt.plot(freqs[mask],cur_min[mask],label="min spectrum")
plt.legend()
plt.yscale('log')
plt.ylabel('Amplitude [mA]')
plt.xlabel('Frequency [Hz]')
plt.grid(True)
plt.show()

