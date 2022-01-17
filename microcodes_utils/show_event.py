#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 18:18:40 2021
@author: daniel

NEW EVENT VIEWER
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import microcodes_modules.functions as fc
from microcodes_modules.events import Event
from microcodes_modules.CAENReader import WDReader
from microcodes_modules.CAENReader import readChannels
from microcodes_modules.auto_plots import histo_stats

optin = {   'in_dir':       'wavesh_211105_1146_70h10',
            'ADC_ch':       int(2**14),
            'nsamp':        1030,
            'deltaT':       4,
            'Vpp':          0.5,
            'ngroups':      1,
            'Nevents':      'ind',
            }

READ = readChannels('DATA/'+optin['in_dir'],Vpp=2.0)
DATA = READ.data()
nevents = READ.nevents()
print('Number of events:', nevents)
file_list = READ.files_list()



ev = 46 # !!! introduce number of event to plot

evento = READ.make_events(ev)

ADC_counts_ev = evento[0].ADC_counts()
mean_ev = np.mean(ADC_counts_ev)
sqdv_ev_sel = fc.sqdev(ADC_counts_ev[644:669],mean_ev)
sqdv_ev = fc.sqdev(ADC_counts_ev,mean_ev)
print(mean_ev,sqdv_ev,sqdv_ev_sel)

fig, ax = plt.subplots(4,2,figsize=(12,16))
fig.suptitle('Plots in time domain of event ' + str(ev))
fig.subplots_adjust(hspace=0.2,wspace=0.2)

# Plot:
for wave in file_list:
    ich = int(wave[-5])
    row = (ich)//2 ;  col = (ich)%2
    
    evento[ich].evn_display(ax[row][col])
    (ax[row][col]).set_xlabel('Time')
    (ax[row][col]).set_ylabel('ADC_count')
    (ax[row][col]).set_xlim(0,4120)
    (ax[row][col]).set_ylim(0,2**14)
    (ax[row][col]).legend()