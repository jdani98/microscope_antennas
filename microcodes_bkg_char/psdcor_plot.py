#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 10:43:27 2021

@author: daniel

PLOT CORRECTED PSD FROM psd_run.py
THE CORRECTION IS THE ELIMINATION OF ATTENUATION DUE TO CABLES
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
in_dir  =    'waves_211108_without_filter'  # !!! name of input directory
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
savefigs = {'event_time':   False,
            'event_freq':   False,
            'histos':       False,
            'PSDs':         True
            }

savepks = False
###############################################################################

# Reading data from csv
file = open('OUTPUTS/'+in_dir+'/'+'data_for_plots.dat','r')
data = csv.reader(file)

ff =        {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
A =         {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
xF_smooth = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
A_smooth =  {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
Ap =        {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}


i = 0
for row in data:
    if (i-0)%11 == 0:
        ch = int(row[0][3])
    if (i-2)%11 == 0:
        ff[ch] = [float(item) for item in row[2:]]
    if (i-7)%11 == 0:
        A[ch] = [float(item) for item in row[2:]]
    if (i-8)%11 == 0:
        xF_smooth[ch] = [float(item) for item in row[2:]]
    if (i-9)%11 == 0:
        A_smooth[ch] = [float(item) for item in row[2:]]
    if (i-10)%11 == 0:
        Ap[ch] = [float(item) for item in row[2:]]
    i+=1
        
file.close()

# Defining attenuation in function of frequency
def atenuation(x,a,b):
    return a*x+b

aten_params = {0:{'a':-0.0685,'b':-2.36},
               1:{'a':-0.0607,'b':-2.34},
               2:{'a':-0.0428,'b':-1.55},
               3:{'a':-0.0429,'b':-1.56},
               4:{'a':-0.0311,'b':-1.07},
               5:{'a':-0.0306,'b':-1.09},
               6:{'a':-0.0265,'b':-0.742},
               7:{'a':-0.0255,'b':-0.745}}

### PLOTS #####################################################################
# PLOT OF POWER SPECTRAL DENSITY
fig4 = plt.figure(4,figsize=(24,9))
fig4.suptitle('Mean Power Spectral Density')
fig4.subplots_adjust(hspace=0.4,wspace=0.2)

minx = 5; maxx = 110
for ich in range(8):
    row = (ich)//4 ;  col = (ich)%4
    ax1 = fig4.add_subplot(11,4,(4*6*row+col+1,4*6*row+col+13))
    ax2 = fig4.add_subplot(11,4,4*6*row+col+17)
    
    for x in np.arange(minx,maxx): ax1.axvline(x=x,color='lightgray',linewidth=0.3)
    ax1.plot(ff[ich],A[ich],color=colors[ich],linewidth=0.3,linestyle='dotted')
    
    A_corr = np.array(A[ich]) - np.array(atenuation(np.array(ff[ich]),aten_params[ich]['a'],aten_params[ich] ['b']))
    A_smooth_corr = np.array(A_smooth[ich]) - np.array(atenuation(np.array(xF_smooth[ich]),aten_params[ich]['a'],aten_params[ich] ['b']))
    ax1.plot(ff[ich],A_corr,color=colors[ich],linewidth=0.3,label='Ch'+str(ich)+' '+orientations[ich])
    ax1.plot(xF_smooth[ich],A_smooth_corr,color=colors[ich],linewidth=0.5,linestyle='dashed',alpha=0.5)
    #ax1.set_xlabel('$f$ (MHz)')
    ax1.set_xticklabels([])
    ax1.set_ylabel('$A$ (dBm/Hz)')
    ax1.set_xlim(minx,maxx)
    ax1.set_ylim(-240,-120)
    ax1.set_xticks(np.arange(minx+5,maxx+5,10))
    ax1.grid()
    ax1.legend()
    
    for x in np.arange(minx,maxx): ax2.axvline(x=x,color='lightgray',linewidth=0.3)
    ax2.plot(xF_smooth[ich],Ap[ich],color=colors[ich],linewidth=0.5,alpha=0.8)
    ax2.set_xlabel('$f$ (MHz)')
    ax2.set_ylabel(r'$\Delta A$')
    ax2.set_xlim(minx,maxx)
    ax2.set_ylim(-20,30)
    ax2.set_xticks(np.arange(minx+5,maxx+5,10))
    ax2.set_yticks([-20,0,20])
    ax2.grid()
plt.show()

if savefigs['PSDs']: plt.savefig('OUTPUTS/'+in_dir+'/'+'PSDs_corr.png',dpi=300)
