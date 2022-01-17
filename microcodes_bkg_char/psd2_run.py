#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 11:27:36 2021
@author: daniel

*** COMPUTATION OF COMPLETE PSDs ***
This program returns a CSV datafile to make:
    -> The PSD (with deviations and phases)

The new data adds to previous data inside the CSV file, making it possible to
record the 8 channels in one single datafile by independent runs.

How to run this file? # !!!
Type in terminal > python3 psd2_run.py [idr] [nch]
where [idr] is the directory with data to read
      [nch] is the number of channel to read
"""

import time

import os
os.chdir('..')
print(os.getcwd())

import sys
idr = str(sys.argv[1])
nch = int(sys.argv[2])

import numpy as np
import cmath
import csv
from scipy.fft import fft, fftfreq

from microcodes_modules.CAENReader import WDReader

time1 = time.time()

### SETTINGS ##################################################################
###### Settings to read data (options in)
in_dir  =    idr                             # name of input directory
nbits   =    14                              # !!! number of bits for ADC channels
nsamp   =    1030                            # !!! number of samples per event
deltaT  =    4                               # !!! real time separation between two samples (ns)
Vpp     =    2.0                             # !!! voltage peak to peak
ADC_ch  =    2**nbits                        # number of ADC_channels, equal to 2**nbits
Fs      =    1/deltaT * 1e9                  # sampling frequency (Hz)
R       =    50                              # input impedance
baseline=    ADC_ch//2                       # baseline

#nch   = input(' Introduce number of channel to read ')
fname = 'wave'+str(nch)+'.dat'

###### Special settings for PSD computation
at_port =    50                              # atenuation portion to apply Hann window

###### Settings to show results (options out)
savepts = True                               # !!! True to save points of figures in csv

###############################################################################

READER = WDReader('DATA/'+in_dir+'/'+fname, channel=nch, nbits=nbits, length=nsamp, dt=deltaT, Vpp=Vpp)
channel, data = READER.autoread()

if savepts:
    os.chdir('OUTPUTS')
    fileslist = os.listdir()
    if in_dir not in fileslist:
        os.mkdir(in_dir)
        print('Created new directory ' + in_dir)


# Complete PSD Spectrum
print('Computing complete PSD ...')
yC = Vpp / 2**14 # counts to V converter
xC = 1.e-6     # Hz to MHz converter
xF = xC * fftfreq(nsamp,deltaT*1.e-9)[:nsamp//2]
A = 0
PHS = complex(0.,0.)
PSDl = []
for iev, event in data.items():
    counts = np.array([yC*count for count in event[1]])
    #counts = half_Hann(counts,at_port,baseline) # debido al alto ruido aleatorio no parece necesario aplicar "windowing"
    
    fft_cpx = fft(counts)[:nsamp//2]
    fft_abs = np.abs(fft_cpx)
    fft_phs = fft_cpx/fft_abs
    
    PSD = (2.0/(nsamp*Fs)) * fft_abs**2  # V^2 / Hz
    Ai = 10 * np.log10(PSD/(R*Fs))
    A += Ai
    
    PHS += fft_phs
    PSDl.append(Ai)

A = A/iev + 30  # final mean PSD in dBm/Hz
PSDl = np.array(PSDl)
sA = [np.std(PSDl[:,i]) for i in range(len(PSDl[0]))] # final stdev for PSD
mean_phs = [cmath.phase(PHSi) for PHSi in PHS] # mean phase
s_phs    = [1. - 1./iev * np.abs(PHSi) for PHSi in PHS] # phase variance

time2 = time.time()

print(' Total time of execution: ', (time2-time1), ' s')
    

# Writing data to csv
if savepts:
    outdata = open(in_dir+'/'+'fullchar.dat','a')
    writer = csv.writer(outdata)
    
    #writer.writerow(['#Ch'+str(channel)])
    
    xF = [item for item in xF]
    A = [item for item in A]
    sA = [item for item in sA]
    m_phs = [item for item in mean_phs]
    s_phs = [item for item in s_phs]
    writer.writerow(['#Ch'+str(channel),'xF']+xF)
    writer.writerow(['#Ch'+str(channel),'A']+A)
    writer.writerow(['#Ch'+str(channel),'sA']+sA)
    writer.writerow(['#Ch'+str(channel),'m_phs']+m_phs)
    writer.writerow(['#Ch'+str(channel),'s_phs']+s_phs)
    
    print(' Data saved into file at OUTPUTS/' + in_dir)
    outdata.close()
