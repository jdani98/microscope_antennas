#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 11:27:36 2021
@author: daniel - Jose Daniel Viqueira Cao

*** COMPUTATION OF HISTOGRAMS OF AMPLITUDES ***
This program returns a CSV datafile to make:
    -> The histogram and all the statistics from ADC counts

The new data adds to previous data inside the CSV file, making it possible to
record the 8 channels in one single datafile by independent runs.

How to run this file? # !!!
Type in terminal > python3 fullchar_run.py [idr] [nch]
where [idr] is the directory with data to read
      [nch] is the number of channel to read
"""

import os
os.chdir('..')
print(os.getcwd())

import sys
idr = str(sys.argv[1])
nch = int(sys.argv[2])

import numpy as np
import csv
from collections import Counter
import scipy.stats as sct

from microcodes_modules.CAENReader import WDReader


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


### Statistics of all signals
print(' ... Computing statistics and histogram')
all_counts = []
for iev, event in data.items():
    all_counts += event[1]
Nev = len(all_counts)

counts = Counter(all_counts)
rango  = np.arange(0,ADC_ch)
histo  = np.array([0]*ADC_ch)
for j in range(len(rango)):
    histo[j] = counts[j]
	
media = np.mean(all_counts)
desvs = np.std(all_counts)
skewn = sct.skew(all_counts)
kurts = sct.kurtosis(all_counts)
maxim = np.max(all_counts)
minim = np.min(all_counts)



### Writing data to csv
if savepts:
    outdata = open(in_dir+'/'+'fullchar.dat','a')
    writer = csv.writer(outdata)
    
    rango = [item for item in rango]
    histo = [item for item in histo]
    writer.writerow(['#Ch'+str(channel),'xh'] + rango)
    writer.writerow(['#Ch'+str(channel),'yh'] + histo)

    writer.writerow(['#Ch'+str(channel),'stats'] + 
                    [Nev,media,desvs,skewn,kurts,maxim,minim])
    
    print(' Data saved into file at OUTPUTS/' + in_dir)
    print(' WARNING. Rows are too large: not recommended to open the file with a text editor')

    outdata.close()
