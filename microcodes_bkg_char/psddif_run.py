#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 13:22:39 2022
@author: daniel

*** COMPUTE DIFFERENCES BETWEEN TWO SPECTRA ***
This program reads two psd spectra and substracts them. Stores the difference
in a csv file with the same format as the inputs.

How to run this file? # !!!
Type in terminal > python3 psddif_run.py [idr1] [idr2]
where [idr1] and [idr2] are the directories with data to subtract: idr1-idr2
"""

import os
os.chdir('..')

import sys
idr1 = str(sys.argv[1])
idr2 = str(sys.argv[2])

import csv


### SETTINGS ##################################################################
###### Settings to read data (options in)
in_dir1 =    idr1                            # name of 1st input directory
in_dir2 =    idr2                            # name of 2nd input directory
nbits   =    14                              # !!! number of bits for ADC channels
nsamp   =    1030                            # !!! number of samples per event
deltaT  =    4                               # !!! real time separation between two samples
Vpp     =    2.0                             # !!! voltage peak to peak
ADC_ch  =    2**nbits                        # number of ADC_channels, equal to 2**nbits
Fs      =    1/deltaT * 1e9                  # sampling frequency (Hz)
R       =    50                              # input impedance
df      =    (Fs/1e6)/nsamp                  # frequency separation of Fourier transforms

fname = 'fullchar.dat'

###### Settings to show results (options out)
savepts = True                               # !!! True to save points of figures in csv

ot_dir = in_dir1+'_U_'+in_dir2 # name of output directory

###############################################################################


if savepts:
    os.chdir('OUTPUTS')
    fileslist = os.listdir()
    if ot_dir not in fileslist:
        os.mkdir(ot_dir)
        print('Created new directory ' + ot_dir)

file1 = open(in_dir1+'/'+'fullchar.dat','r')
data1 = csv.reader(file1)
file2 = open(in_dir2+'/'+'fullchar.dat','r')
data2 = csv.reader(file2)

xF1     = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
A1      = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
xF2     = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
A2      = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}

xF      = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
dA      = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}

for row in data1:
    ch = int(row[0][3])
    if row[1] == 'xF':
        xF1[ch] = [float(item) for item in row[3:]]
    if row[1] == 'A':
        A1[ch] = [float(item) for item in row[3:]]

for row in data2:
    ch = int(row[0][3])
    if row[1] == 'xF':
        xF2[ch] = [float(item) for item in row[3:]]
    if row[1] == 'A':
        A2[ch] = [float(item) for item in row[3:]]

for ich in range(8):
    if (xF1[ich][0] - xF2[ich][0]) < df:
        xF[ich] = [(item1+item2)/2 for (item1,item2) in zip(xF1[ich],xF2[ich])]
        dA[ich] = [(item1-item2) for (item1,item2) in zip(A1[ich],A2[ich])]


# Writing data to csv
if savepts:
    outdata = open(ot_dir+'/'+'fullchar.dat','a')
    writer = csv.writer(outdata)
    
    for ich in range(8):
        xf = [item for item in xF[ich]]
        da = [item for item in dA[ich]]
        writer.writerow(['#Ch'+str(ich),'xF']+xf)
        writer.writerow(['#Ch'+str(ich),'A']+da)

    
    print(' Data saved into file at OUTPUTS/' + ot_dir)
    outdata.close()