#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 18:03:55 2022
@author: daniel

*** READING OF AN EVENT'S AMPLITUDES AND COMPUTATION OF FOURIER TRANSFORM ***
This program returns a CSV datafile to obtain:
    -> The time domain of an event
    -> The frequency domain of an event

The new data adds to previous data inside the CSV file, making it possible to
record the 8 channels in one single datafile by independent runs.

How to run this file? # !!!
Type in terminal > python3 fullchar_run.py [idr] [nch]
where [idr] is the directory with data to read (write it in quotes)
      [nch] is the number of channel to read
      [sev] is the number of event to record
"""

import os
os.chdir('..')
print(os.getcwd())

import sys
idr = str(sys.argv[1])
nch = int(sys.argv[2])
sev = int(sys.argv[3])

import csv
import microcodes_modules
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

evento = READER.make_events(sev)

# Data to plot one event in time domain
print(' ... Computing one event')
t = evento.smp_times()
y = evento.ADC_counts()


# Data to plot one event in frequency domain
ff,yf = evento.fourier()



### Writing data to csv
if savepts:
    outdata = open(in_dir+'/'+'fullchar.dat','a')
    writer = csv.writer(outdata)
    
    t = [item for item in t]
    y = [item for item in y]
    writer.writerow(['#Ch'+str(channel),sev,'t_ev'] + t)
    writer.writerow(['#Ch'+str(channel),sev,'y_ev'] + y)

    ff = [item for item in ff]
    yf = [item for item in yf]
    writer.writerow(['#Ch'+str(channel),sev,'ff_ev'] + ff)
    writer.writerow(['#Ch'+str(channel),sev,'yf_ev'] + yf)
    
    outdata.close()
