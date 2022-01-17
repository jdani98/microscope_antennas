#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 18:28:06 2021
@author: daniel

*** PLOT OF HISTOGRAMS OF AMPLITUDES ***
This program reads CSV datafiles 'fullchar.dat' to plot:
    -> Histograms of amplitudes and statistics

How to run this file? # !!!
Type in terminal > python3 histo_plot.py [idr]
where [idr] is the directory with data to read
"""

import os
os.chdir('..')

import sys
idr = str(sys.argv[1])

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import csv

colors = cm.tab10(np.linspace(0,1,8))
orientations = {0:'EW', 1:'NS', 2:'NS', 3:'EW', 4:'EW', 5:'NS', 6:'NS', 7:'EW'}
### SETTINGS ##################################################################
###### Settings to read data (options in)
in_dir  =    idr                             # !!! name of input directory
nbits   =    14                              # !!! number of bits for ADC channels
nsamp   =    1030                            # !!! number of samples per event
deltaT  =    4                               # !!! real time separation between two samples
Vpp     =    2.0                             # !!! voltage peak to peak
ADC_ch  =    2**nbits                        # number of ADC_channels, equal to 2**nbits
Fs      =    1/deltaT * 1e9                  # sampling frequency (Hz)
R       =    50                              # input impedance

###### Settings to show results (options out)
showfigs = False
savefigs = {'Horizontal': True,
            'Vertical':   True}

###############################################################################

# Reading data from csv
file = open('OUTPUTS/'+in_dir+'/'+'fullchar.dat','r')
data = csv.reader(file)

xh =        {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
yh =        {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
stats =     {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}


for row in data:
    ch = int(row[0][3])
    if row[1] == 'xh':
        xh[ch]  = [int(item) for item in row[2:]]
    if row[1] == 'yh':
        yh[ch] = [int(item) for item in row[2:]]
    if row[1] == 'stats':
        stats[ch] = [float(item) for item in row[2:]]
        
file.close()


### PLOTS #####################################################################
plt.close('all')

# Content of PLOT OF HISTOGRAM AND STATISTICS
def plot_histo(ax,ich):
    ax.plot(xh[ich],yh[ich],linewidth=0.5,color=colors[ich],label='Ch'+str(ich)+' '+orientations[ich])
    texto = ('n: %i \nmean: %6.2f \nstd: %6.2f \nskwn: %6.2f \nkurt: %6.2f \nmax: %i \nmin: %i' 
                 %tuple(stats[ich]))
    props = dict(boxstyle='round',color='gainsboro',fill=True,alpha=0.5)
    ax.text(0.05, 0.8, texto, horizontalalignment='left', verticalalignment='center', 
                            bbox=props, transform=ax.transAxes, size='x-small')
    return


if showfigs:
    # Interactive figure of HISTOGRAM AND STATISTICS
    fig11 = plt.figure(1,figsize=(16,9))
    fig11.suptitle('Histogram and statistics of amplitudes')
    fig11.subplots_adjust(hspace=0.2,wspace=0.4)

    for ich in range(8):
        ax = fig11.add_subplot(2,4,ich+1)
        plot_histo(ax,ich)
        ax.set_xlabel('ADC amplitude')
        ax.set_ylabel('counts')
        ax.set_xlim(0,2**nbits)
        #ax.grid()
        ax.legend()
    plt.show()


if savefigs['Horizontal']:
    # Horizontal figure to save of HISTOGRAM AND STATISTICS
    fig12 = plt.figure(2,figsize=(18,9))
    fig12.suptitle('Histogram and statistics of amplitudes')
    fig12.subplots_adjust(hspace=0.1,wspace=0.2)

    for ich in range(8):
        ax = fig12.add_subplot(2,4,ich+1)
        plot_histo(ax,ich)
        if ich//4==1: ax.set_xlabel('ADC amplitude')
        if ich%4==0:  ax.set_ylabel('counts')
        ax.set_xlim(0,2**nbits)
        #ax.grid()
        ax.legend()
        
    plt.savefig('OUTPUTS/'+in_dir+'/'+'histo_169.png',dpi=300,bbox_inches='tight')


if savefigs['Vertical']:
    # Vertical figure to save of HISTOGRAM AND STATISTICS
    fig13 = plt.figure(3,figsize=(10.5,14.85))
    fig13.subplots_adjust(hspace=0.2,wspace=0.2)

    for ich in range(8):
        ax = fig13.add_subplot(4,2,ich+1)
        plot_histo(ax,ich)
        if ich//2==3: ax.set_xlabel('ADC amplitude')
        if ich%2==0:  ax.set_ylabel('counts')
        ax.set_xlim(0,2**nbits)
        #ax.grid()
        ax.legend()
        
    plt.savefig('OUTPUTS/'+in_dir+'/'+'histo_A4.png',dpi=300,bbox_inches='tight')
