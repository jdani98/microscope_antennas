#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 13:46:47 2021
@author: daniel

*** COMPUTATION OF mPSD IN GROUPS ***
This program returns a CSV datafile to make:
    -> The evolution of the mean PSD (with deviations and phases)

The new data adds to previous data inside the CSV file, making it possible to
record the 8 channels in one single datafile by independent runs.

How to run this file? # !!!
Type in terminal > python3 psd24h_run.py [idr] [nch]
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
Vpp     =    0.5                             # !!! voltage peak to peak
ADC_ch  =    2**nbits                        # number of ADC_channels, equal to 2**nbits
Fs      =    1/deltaT * 1e9                  # sampling frequency (Hz)
R       =    50                              # input impedance
baseline=    ADC_ch//2                       # baseline

#nch   = input(' Introduce number of channel to read ')
fname = 'wave'+str(nch)+'.dat'

###### Settings of timing and agrupation of events
DeltaT  =    2                               # time between two events (in seconds)
nevnts  =    900                             # number of events per group
timegr  =    DeltaT*nevnts                   # duration of one group

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

Nev = len(data)
print('Number of events: ', Nev)


# Complete PSD Spectrum
print('Computing complete PSD ...')
yC = Vpp / 2**14 # counts to V converter
xC = 1.e-6     # Hz to MHz converter
xF = xC * fftfreq(nsamp,deltaT*1.e-9)[:nsamp//2]


Ng = Nev//nevnts

A = [] ;  sA = [] ;  m_phs = [] ;  s_phs = []
for ig in range(Ng):
    PHS = complex(0.,0.)
    PSDl = []
    for iev in range(ig*nevnts,(ig+1)*nevnts):
        bulk = data[iev][1]
        counts = np.array([yC*count for count in bulk])
    
        fft_cpx = fft(counts)[:nsamp//2]
        fft_abs = np.abs(fft_cpx)
        fft_phs = fft_cpx/fft_abs
    
        PSD = (2.0/(nsamp*Fs)) * fft_abs**2  # V^2 / Hz
        Ai = 10 * np.log10(PSD/(R*Fs))
    
        PHS += fft_phs
        PSDl.append(Ai)

    PSDl = np.array(PSDl)
    A_ig = [np.mean(PSDl[:,i]) for i in range(len(PSDl[0]))] # final mean  for PSD
    sA_ig = [np.std(PSDl[:,i]) for i in range(len(PSDl[0]))] # final stdev for PSD
    A.append(A_ig)
    sA.append(sA_ig)
    
    mean_phs_ig = [cmath.phase(PHSi) for PHSi in PHS] # mean phase
    s_phs_ig    = [1. - 1./iev * np.abs(PHSi) for PHSi in PHS] # phase variance
    m_phs.append(mean_phs_ig)
    s_phs.append(s_phs_ig)

time2 = time.time()

print(' Total time of execution: ', (time2-time1), ' s')


# Writing data to csv
if savepts:
    outdata = open(in_dir+'/'+'psd24h.dat','a')
    writer = csv.writer(outdata)
    
    writer.writerow(['#Ch'+str(channel),'head',DeltaT,nevnts,timegr])
    xF = [item for item in xF]
    writer.writerow(['#Ch'+str(channel),'xF']+xF)
    
    for ig in range(Ng):
        time_block = ig*timegr/60
        A_ig = [item for item in A[ig]]
        sA_ig = [item for item in sA[ig]]
        m_phs_ig = [item for item in m_phs[ig]]
        s_phs_ig = [item for item in s_phs[ig]]
        writer.writerow(['#Ch'+str(channel),'A',time_block]+A_ig)
        writer.writerow(['#Ch'+str(channel),'sA',time_block]+sA_ig)
        writer.writerow(['#Ch'+str(channel),'m_phs',time_block]+m_phs_ig)
        writer.writerow(['#Ch'+str(channel),'s_phs',time_block]+s_phs_ig)
    
    print(' Data saved into file at OUTPUTS/' + in_dir)
    outdata.close()
