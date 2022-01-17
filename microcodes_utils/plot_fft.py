#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 10:20:40 2021
@author: daniel

VISUALIZATION OF ONE EVENT'S AMPLITUDES AND FOURIER TRANSFORM
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from microcodes_modules.CAENReader import readChannels
from microcodes_modules.events import Event

colors = ['b','g','r','c','m','y','k','tab:gray']

###### Settings to read data (options in)
""" Legend:
	* in_dir -> name of input directory
	* ADC_ch -> number of ADC channels, equal to 2^Nbits
	* nsamp -> number of samples per event
	* deltaT -> real time separation between two samples
	* Vpp -> voltage peak to peak
	* ngroups -> number of groups to study data
	* Nevents -> number of events per group
"""
optin = {	'in_dir':		'wavesh_211018_1812_0h02',
			'ADC_ch':		int(2**14),
			'nsamp':		1030,
            'deltaT':       4,
            'Vpp':          0.5,
            'ngroups':      1,
            'Nevents':      'ind',
			}

###### Settings to show results (options out)
optot = {	
		}
######

#####
cntr_of_fwin = optin['nsamp']/2 # Here is the trigger
# Delays induced by the travel of signals by the cable from antennas to digitizer:
cable_delays = np.array([576.5,574.8,403.0,403.0,286.5,284.7,209.0,207.2]) # ns
# Time of particles from antennas height to floor (where scintillator is)
particle_delay = 30 #ns
# Approximated time of delay of trigger
trigger_delay = 30 #ns
# Total expected pulse delay = cable_delays - particle_delay - trigger_delay
total_delay = cable_delays - particle_delay - trigger_delay
print('Total delay for each channel: ', total_delay, '\n')

win = 100 # width of window in ns. Must be multiple of 4
for i,item in optin.items(): print('%10s: %s' %(i,str(item)))
#####

READ = readChannels('DATA/'+optin['in_dir'],Vpp=0.5)
DATA = READ.data()
nevents = READ.nevents()
print('Number of events:', nevents)
file_list = READ.files_list()
print(file_list)


sev = input('Introduce number of event(s) to visualize ')
lev = sev.split(); lev = [int(levi) for levi in lev]
print(lev)
for iev in lev:
    
    fig, ax = plt.subplots(4,2,figsize=(12,16))
    fig.suptitle('Plots in time domain of event ' + str(iev))
    fig.subplots_adjust(hspace=0.2,wspace=0.2)

    for wave in file_list:
        ich = int(wave[-5])
        row = (ich)//2 ;  col = (ich)%2
        
        channel, data = DATA[ich][iev]
        evento = Event(data,channel=ich)
    
        winini = total_delay[ich]
        (ax[row][col]).axvline(x=winini,linestyle='--',color='tab:red',linewidth=0.5)
        R = patch.Rectangle((total_delay[ich],0),win,2**14,color='gray',alpha=0.2)
        (ax[row][col]).add_patch(R)
    
        evento.evn_display(ax[row][col])
        (ax[row][col]).set_xlabel('Time')
        (ax[row][col]).set_ylabel('ADC_count')
        (ax[row][col]).set_xlim(0,4120)
        (ax[row][col]).set_ylim(0,2**14)
        (ax[row][col]).legend()
    
    fig0, ax0 = plt.subplots(4,2,figsize=(12,16))
    fig0.suptitle('Plots in frequency domain of event ' + str(iev))
    fig0.subplots_adjust(hspace=0.2,wspace=0.2)

    for wave in file_list:
        ich = int(wave[-5])
        row = (ich)//2 ;  col = (ich)%2
        
        channel, data = DATA[ich][iev]
        evento = Event(data,channel=ich)
    
        evento.evn_display_fourier(ax0[row][col])
        (ax0[row][col]).set_xlabel('Frequency (MHz)')
        (ax0[row][col]).set_ylabel('au')
        (ax0[row][col]).set_xlim(10,90)
        (ax0[row][col]).set_ylim(0,0.05)
        (ax0[row][col]).legend()