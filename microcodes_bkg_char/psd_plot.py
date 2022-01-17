#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 18:42:13 2022
@author: daniel

*** PLOT OF MEAN POWER SPECTRAL DENSITY ***
This program reads CSV datafiles 'fullchar.dat' to plot:
    -> Mean Power Spectral Density (ax1 in fig1)

How to run this file? # !!!
Type in terminal > python3 psd_plot.py [idr]
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
import microcodes_modules.functions as fc

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
minx = 5; maxx = 500; stp = 50 # !!! limits of frequency & step of xticks
ax1_miny = 0; ax1_maxy = 120  # !!! limits of y axis in ax1
showfigs = False
savefigs = {'Horizontal': True,
            'Vertical':   True}

###############################################################################

# Reading data from csv
file = open('OUTPUTS/'+in_dir+'/'+'fullchar.dat','r')
data = csv.reader(file)

xF =        {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
A =         {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}

for row in data:
    ch = int(row[0][3])
    if row[1] == 'xF':
        xF[ch]  = [float(item) for item in row[2:]]
    if row[1] == 'A':
        A[ch]  = [float(item) for item in row[2:]]

file.close()



### PLOTS #####################################################################
plt.close('all')

# Content of PLOT OF POWER SPECTRAL DENSITY
def plot_psd(ax,ich):
    ax.plot(xF[ich],A[ich],color=colors[ich],linewidth=1.0,label='Ch'+str(ich)+' '+orientations[ich])
    return

# Set of x axis
def xtik_psd(ax,ich):
    for x in np.arange(minx,maxx,stp//10): ax.axvline(x=x,color='lightgray',linewidth=0.3)
    ax.set_xlim(minx,maxx)
    ax.set_xticks(np.arange(stp,maxx+1,stp))
    return

if showfigs:
    # Interactive figure OF POWER SPECTRAL DENSITY
    fig11 = plt.figure(1,figsize=(16,9))
    fig11.suptitle('Mean Power Spectral Density')
    fig11.subplots_adjust(hspace=0.2,wspace=0.4)

    for ich in range(8):
        row = (ich)//4 ;  col = (ich)%4
        ax1 = fig11.add_subplot(2,4,ich+1)
    
        xtik_psd(ax1,ich)
        plot_psd(ax1,ich)
        ax1.set_ylim(ax1_miny,ax1_maxy) # !!! ylims
        #ax1.set_yticks([-230,-210,-190,-170,-150])
        ax1.set_xlabel('$f$ (MHz)')
        ax1.set_ylabel('$A$ (dBm/Hz)')
        ax1.grid()
        ax1.legend()
    plt.show()


if savefigs['Horizontal']:
    # Vertical figure to save OF POWER SPECTRAL DENSITY
    fig12 = plt.figure(2,figsize=(18,9))
    fig12.suptitle('Mean Power Spectral Density')
    fig12.subplots_adjust(hspace=0.1,wspace=0.2)

    for ich in range(8):
        ax1 = fig12.add_subplot(2,4,ich+1)
        xtik_psd(ax1,ich)
        plot_psd(ax1,ich)
        ax1.set_ylim(ax1_miny,ax1_maxy)
        #ax1.set_yticks([-230,-210,-190,-170,-150])
        if ich//4==1: ax1.set_xlabel('$f$ (MHz)')
        if ich%4==0:  ax1.set_ylabel('$A$ (dBm/Hz)')
        ax1.grid()
        ax1.legend()

    plt.savefig('OUTPUTS/'+in_dir+'/'+'psd_169.png',dpi=300,bbox_inches='tight')


if savefigs['Vertical']:
    # Horizontal figure to save OF POWER SPECTRAL DENSITY
    fig13 = plt.figure(3,figsize=(10.5,14.85))
    fig13.subplots_adjust(hspace=0.2,wspace=0.2)

    for ich in range(8):
        ax1 = fig13.add_subplot(4,2,ich+1)
        xtik_psd(ax1,ich)
        plot_psd(ax1,ich)
        ax1.set_ylim(ax1_miny,ax1_maxy)
        #ax1.set_yticks([-230,-210,-190,-170,-150])
        if ich//2==3: ax1.set_xlabel('$f$ (MHz)')
        if ich%2==0:  ax1.set_ylabel('$A$ (dBm/Hz)')
        ax1.grid()
        ax1.legend()

    plt.savefig('OUTPUTS/'+in_dir+'/'+'psd_A4.png',dpi=300,bbox_inches='tight')
