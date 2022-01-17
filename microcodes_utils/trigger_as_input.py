#!usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 19∶48∶19 2021
@author: daniel

ESTIMATION OF DELAYS OF TRIGGER AND PLOT OF SIGNAL
FOR FILES WITH TRIGGER AS INPUT
"""


import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('..')
from collections import Counter

import struct

import microcodes_modules.functions as fc

options = {	'in_dir':		'DATA/trigger_as_input2',
			'ADC_ch':		int(2**14),
			'nsamp':		1030,
            'deltaT':       4,
            'Vpp':          0.5,
            'ngroups':      1,
            'Nevents':      'ind',
            'Show_plot1':   False,
            'Show_plot2':   True
			}

baseline = options['ADC_ch']*0.5
cwd = os.getcwd()  # main current working directory
os.chdir(cwd+'/'+options['in_dir'])

fname = 'wave0(2).dat'

data  = np.fromfile(fname, dtype='<i2')
dat_ag= fc.agrupar(data,options['nsamp'])

print('Number of events: ', len(dat_ag))

threshold = -100
direction = 'negative'

triggers = []
for event in dat_ag:
	trigger_times = []
	for i,sample in enumerate(event):
		if sample<(baseline+threshold):
			trigger_times.append(i*options['deltaT'])
	triggers.append(trigger_times)

triggers_start = [item[0] for item in triggers]
print(triggers_start)

mean_start = np.mean(triggers_start)
std_start  = np.std(triggers_start)

expected_mean = options['nsamp']*options['deltaT']/2
expected_std  = options['deltaT']/np.sqrt(12)

print('mean (real/expected): ', mean_start,expected_mean)
print('std  (real/expected): ', std_start,expected_std)

possible_delay = expected_mean - mean_start
print('possible delay: ', np.round(possible_delay,2), ' ns')

ev = int(input('Number of event '))

time = np.arange(0,options['nsamp']*options['deltaT'],options['deltaT'])

plt.figure(1)
plt.plot(time,dat_ag[ev])
plt.axhline(y=baseline,color='red',linestyle='--',linewidth=0.5)
plt.xlim(0,4120)
plt.ylim(0,16000)
plt.xlabel('Time (ns)')
plt.ylabel('ADC channels')
plt.grid()
plt.show()
