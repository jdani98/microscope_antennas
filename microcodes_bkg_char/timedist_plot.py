#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 17:17:06 2021

@author: daniel
*** READING data_for_time_histos TO MAKE THE PLOTS ***
"""

import os
os.chdir('..')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import csv

colors = cm.tab10(np.linspace(0,1,8))
orientations = {0:'EW', 1:'NS', 2:'NS', 3:'EW', 4:'EW', 5:'NS', 6:'NS', 7:'EW'}

### SETTINGS ##################################################################
###### Settings to read data (options in)
in_dir  =    'waves_211104_0950_continuous'    # !!! name of input directory
nbits   =    14                              # !!! number of bits for ADC channels
nsamp   =    1030                            # !!! number of samples per event
deltaT  =    4                              # !!! real time separation between two samples
Vpp     =    2.0                             # !!! voltage peak to peak
ADC_ch  =    2**nbits                        # number of ADC_channels, equal to 2**nbits
Fs      =    1/deltaT * 1e9                  # sampling frequency (Hz)
R       =    50                              # input impedance
ngroups =    1                               # number of groups to study data
Nevents =    'ind'                           # number of events per group

###### Settings to show results (options out)
savefigs = {'event_time':   True,
            'event_freq':   True,
            'histos':       True,
            'PSDs':         True
            }

savepks = True
###############################################################################

time_interval = 412 # !!! introduce manually time interval of each bin

# Reading data from csv
file = open('OUTPUTS/'+in_dir+'/'+'time_histos.dat','r')
data = csv.reader(file)

time =         {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
hist =         {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}

i = 0
for row in data:
    if (i-0)%3 == 0:
        ch = int(row[0][3])
    if (i-1)%3 == 0:
        time[ch]  = [float(item) for item in row]
    if (i-2)%3 == 0:
        hist[ch] = [float(item) for item in row]
    i += 1


### PLOTS #####################################################################
plt.close('all')
fig, ax = plt.subplots(4,2,figsize=(12,16))
fig.suptitle('Histograms of standard deviations')
fig.subplots_adjust(hspace=0.2,wspace=0.6)

for ich in range(8):
    row = (ich)//2 ;  col = (ich)%2

    #(ax[row][col]).plot(time,histo[ich],'o')
    (ax[row][col]).bar(time[ich],hist[ich],label='Ch '+str(ich),width=0.8*time_interval)
    (ax[row][col]).set_xlabel('time')
    (ax[row][col]).set_ylabel('counts')
    maxi = max(hist[ich])
    print(maxi)
    #(ax[row][col]).set_ylim(0.99*maxi,1.001*maxi)
    (ax[row][col]).legend()