"""
Created on Mon Feb 15 19:29:56 2021
This script loads bpm readings [[x],[y]] from aqcfile+'.pickle' and the response 
matrix present in 'Rmat.pickle' file.

After calculating the pseudoinverse of Rmat through SVD, the current response is obtained from 
R_pseudoinv @ xy_read/kick_factor, with kick_factor = 0.03 urad/mA

FFT are calculated for FOFB acq rate

Results in time domain are dumped to acqfile+'i_FCOR.pickle' in mA

@author: henrique.caiafa
"""
import pickle
import numpy as np
import scipy.io
import matplotlib.pyplot as plt

acqfile = input('Insert .pickle I/O filename (without extension): ')

with open('Rmat.pickle', 'rb') as filehandle:
    Rmat = pickle.load(filehandle)    # [um/urad]
    
U, s, Vt = np.linalg.svd(Rmat)

threshold = 1e-5

s_inv = np.array([1/i if i > threshold else 0. for i in s])

W_inv = np.zeros((len(Vt), len(U))) #, dtype=complex)
W_inv[:len(Vt), :len(Vt)] = np.diag(s_inv)

R_pseudoinv = np.linalg.multi_dot([np.transpose(Vt), W_inv, np.transpose(U)])

fRF = 499.6649e6

fFOFB = fRF/19872
wFOFB = 2*np.pi*fFOFB

Ts = 1/fFOFB

with open(acqfile + '.pickle', 'rb') as filehandle2:
    xy_read = pickle.load(filehandle2)*1e-3

_,ns = xy_read.shape

kick_factor = 0.03 # urad/mA
corr_signals = R_pseudoinv @ xy_read/kick_factor 

# plot correctors' time signals (largest std vs lowest std value)

corr_signals_std = np.std(corr_signals,axis=1)

min_index = np.argmin(corr_signals_std)
max_index = np.argmax(corr_signals_std)

t = np.linspace(0.,ns*Ts,ns)

plt.figure(1)
plt.plot(t,corr_signals[max_index],t,corr_signals[min_index])

# FFT of the results

freqs = np.fft.fftfreq(ns)*fFOFB
mask = freqs > 0  # list with indexes 

cur_spectra =  np.array( [ 2.0*np.abs(np.fft.fft(corr_signals[i])/ns) for i in range(len(R_pseudoinv)) ] )

# mean and max collumn-wise (i.e. for each fft bin)
cur_mean = np.mean(cur_spectra,axis=0)
cur_max = np.max(cur_spectra,axis=0)

plt.figure(2)

plt.plot(freqs[mask],cur_max[mask],label="max bin values")
plt.plot(freqs[mask],cur_mean[mask],label="avg spectrum")

plt.legend()
plt.yscale('log')
plt.ylabel('Amplitude [mA]')
plt.xlabel('Frequency [Hz]')
plt.grid(True)
plt.show()

# Dumping result to files

with open( acqfile + '_i_FCOR.pickle','wb') as filewrite:
    # store the data as binary data stream
    pickle.dump(corr_signals, filewrite ) 

scipy.io.savemat('./' + acqfile + '_i_FCOR.mat', mdict={'corr_signals': corr_signals})