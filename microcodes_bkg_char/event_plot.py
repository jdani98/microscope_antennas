#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 18:22:32 2022
@author: daniel

*** PLOT OF AN EVENT'S AMPLITUDES AND FOURIER TRANSFORM ***
This program reads CSV datafiles 'fullchar.dat' to plot:
    -> The time domain of an event
    -> The frequency domain of an event

How to run this file? # !!!
Type in terminal > python3 event_plot.py [idr]
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
minx = 5; maxx = 110  # limits of frequencies in Fourier transform plots
showfigs = False
savefigs = {'Horizontal': True,
            'Vertical':   True }

###############################################################################

# Reading data from csv
file = open('OUTPUTS/'+in_dir+'/'+'fullchar.dat','r')
data = csv.reader(file)


t =         {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
y =         {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
ff =        {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
yf =        {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}

for row in data:
    ch  = int(row[0][3])
    if row[2] == 't_ev':
        iev = int(row[1])
        t[ch]  = [int(item) for item in row[3:]]
    if row[2] == 'y_ev':
        iev = int(row[1])
        y[ch]  = [int(item) for item in row[3:]]
    if row[2] == 'ff_ev':
        iev = int(row[1])
        ff[ch]  = [float(item) for item in row[3:]]
    if row[2] == 'yf_ev':
        iev = int(row[1])
        yf[ch]  = [float(item) for item in row[3:]]


### PLOTS #####################################################################
plt.close('all')

# Content of PLOT IN TIME DOMAIN:
def plot_time(ax,ich):
    ax.plot(t[ich],y[ich],linewidth=0.5,color=colors[ich],label='Ch'+str(ich)+' '+orientations[ich])
    return

# Content of PLOT IN FREQUENCY DOMAIN:
def plot_freq(ax,ich):
    ax.plot(ff[ich][1:],yf[ich][1:],linewidth=0.5,color=colors[ich],label='Ch'+str(ich)+' '+orientations[ich])
    return


if showfigs:
    # Interactive figure OF ONE EVENT IN TIME DOMAIN:
    fig11 = plt.figure(1,figsize=(16,9))
    fig11.suptitle('Plots in time domain of event'+str(iev))
    fig11.subplots_adjust(hspace=0.2,wspace=0.4)
    for ich in range(8):
        ax = fig11.add_subplot(2,4,ich+1)
        plot_time(ax,ich)
        ax.set_xlabel('Time (ns)')
        ax.set_ylabel('ADC amplitude')
        ax.set_xlim(0,nsamp*deltaT)
        ax.set_ylim(0,2**nbits)
        #ax.grid()
        ax.legend()

    # Interactive figure OF ONE EVENT IN FREQUENCY DOMAIN:
    fig21 = plt.figure(2,figsize=(16,9))
    fig21.suptitle('Plots in frequency domain of event'+str(iev))
    fig21.subplots_adjust(hspace=0.2,wspace=0.4)
    for ich in range(8):
        ax = fig21.add_subplot(2,4,ich+1)
        plot_freq(ax,ich)
        ax.set_xlabel('Frequency (MHz)')
        ax.set_ylabel('$A$ (V/Hz)')
        ax.set_xlim(minx,maxx)
        #ax.set_ylim(0,0.5)
        #ax.grid()
        ax.legend()

    plt.show()


if savefigs['Horizontal']:
    # Horizontal figure to save OF ONE EVENT IN TIME DOMAIN:
    fig12 = plt.figure(3,figsize=(18,9))
    fig12.suptitle('Plots in time domain of event'+str(iev))
    fig12.subplots_adjust(hspace=0.1,wspace=0.2)
    for ich in range(8):
        ax = fig12.add_subplot(2,4,ich+1)
        plot_time(ax,ich)
        if ich//4==1: ax.set_xlabel('Time (ns)')
        if ich%4==0:  ax.set_ylabel('ADC amplitude')
        ax.set_xlim(0,nsamp*deltaT)
        ax.set_ylim(0,2**nbits)
        #ax.grid()
        ax.legend()
    plt.savefig('OUTPUTS/'+in_dir+'/event_time_169.png',dpi=300,bbox_inches='tight')

    # Horizontal figure to save OF ONE EVENT IN FREQUENCY DOMAIN:
    fig22 = plt.figure(4,figsize=(18,9))
    fig22.suptitle('Plots in frequency domain of event'+str(iev))
    fig22.subplots_adjust(hspace=0.1,wspace=0.2)
    for ich in range(8):
        ax = fig22.add_subplot(2,4,ich+1)
        plot_freq(ax,ich)
        if ich//4==1: ax.set_xlabel('Frequency (MHz)')
        if ich%4==0:  ax.set_ylabel('$A$ (V/Hz)')
        ax.set_xlim(minx,maxx)
        #ax.set_ylim(0,0.5)
        #ax.grid()
        ax.legend()
    plt.savefig('OUTPUTS/'+in_dir+'/event_freq_169.png',dpi=300,bbox_inches='tight')


if savefigs['Vertical']:
    # Horizontal figure to save OF ONE EVENT IN TIME DOMAIN:
    fig13 = plt.figure(5,figsize=(10.5,14.85))
    fig13.subplots_adjust(hspace=0.2,wspace=0.2)
    for ich in range(8):
        ax = fig13.add_subplot(4,2,ich+1)
        plot_time(ax,ich)
        if ich//2==3: ax.set_xlabel('Time (ns)')
        if ich%2==0:  ax.set_ylabel('ADC amplitude')
        ax.set_xlim(0,nsamp*deltaT)
        ax.set_ylim(0,2**nbits)
        #ax.grid()
        ax.legend()
    plt.savefig('OUTPUTS/'+in_dir+'/event_time_A4.png',dpi=300,bbox_inches='tight')

    # Horizontal figure to save OF ONE EVENT IN FREQUENCY DOMAIN:
    fig23 = plt.figure(6,figsize=(10.5,14.85))
    fig23.subplots_adjust(hspace=0.2,wspace=0.2)
    for ich in range(8):
        ax = fig23.add_subplot(4,2,ich+1)
        plot_freq(ax,ich)
        if ich//2==3: ax.set_xlabel('Frequency (MHz)')
        if ich%2==0:  ax.set_ylabel('$A$ (V/Hz)')
        ax.set_xlim(minx,maxx)
        #ax.set_ylim(0,0.5)
        #ax.grid()
        ax.legend()
    plt.savefig('OUTPUTS/'+in_dir+'/event_freq_A4.png',dpi=300,bbox_inches='tight')
