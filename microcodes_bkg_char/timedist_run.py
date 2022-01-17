#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 16:47:39 2021

@author: daniel
*** READING DATA TO THEN PLOT TIME HISTOGRAMS ***
"""

import os
os.chdir('..')
print(os.getcwd())

import sys
nch = int(sys.argv[1])

import numpy as np
#import matplotlib.pyplot as plt
import csv
#from collections import Counter
#import scipy.stats as sct
#from scipy.fft import fft, fftfreq
#import scipy.fftpack as fourier

import modules_for_python.functions as fc
from modules_for_python.CAENReader import WDReader
#from modules_for_python.CAENReader import readChannels
#from modules_for_python.events import Event
#from modules_for_python.auto_plots import histo_stats


### SETTINGS ##################################################################
###### Settings to read data (options in)
in_dir  =    'waves_211104_0950_continuous'    # !!! name of input directory
nbits   =    14                              # !!! number of bits for ADC channels
nsamp   =    1030                            # !!! number of samples per event
deltaT  =    4                              # !!! real time separation between two samples (ns)
Vpp     =    0.5                             # !!! voltage peak to peak
ADC_ch  =    2**nbits                        # number of ADC_channels, equal to 2**nbits
Fs      =    1/deltaT * 1e9                  # sampling frequency (Hz)
R       =    50                              # input impedance
ngroups =    1                               # number of groups to study data
Nevents =    'ind'                           # number of events per group

#nch   = input(' Introduce number of channel to read ')
fname = 'wave'+str(nch)+'.dat'

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


time_interval = 412 # !!! introduce time interval of histogram bins
samp_interval = time_interval//deltaT
print('samples interval: ', samp_interval)
nbins = int(nsamp/samp_interval)
print('number of bins: ', nbins)
time = [(i+0.5)*time_interval for i in range(nbins)]


histo = np.array([0.0]*nbins)
for iev, event0 in data.items():
    event = event0[1]
    mean_all = np.mean(event) 
    for i in range(nbins):
        piece = event[i*samp_interval:(i+1)*samp_interval]
        sqrdev = fc.sqdev(piece,mean_all)
        histo[i] += sqrdev

# Writing data to csv
if savepts:
    outdata = open(in_dir+'/'+'time_histo.dat','a')
    writer = csv.writer(outdata)
    writer.writerow(['#Ch'+str(channel)])
    writer.writerow(time)
    writer.writerow(histo)