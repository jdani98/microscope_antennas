#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 18:35:43 2021
@author: daniel

TRANSFORM TO DECIMATION FACTOR 2
"""

import struct
import numpy as np
import os
os.chdir('..')
cwd = os.getcwd()
print(cwd)

import sys
nch = int(sys.argv[1])

### SETTINGS ##################################################################
###### Settings to read data (options in)
in_dir  =    'waves_211116_1035_4096samp'     # !!! name of input directory
decfac  =    4                                # !!! decimation factor
###############################################################################


infile = np.fromfile('DATA/'+in_dir+'/'+'wave'+str(nch)+'.dat',dtype='i2')
otfile = open('DATA/'+in_dir+'/'+'wave'+str(nch)+'_x'+str(decfac)+'.dat','wb')

i = 0
newsamp = 0
for samp in infile:
	newsamp += samp
	if (i+1)%decfac == 0:
		newsamp = int(newsamp/decfac)
		otfile.write(struct.pack('h',newsamp))
		newsamp = 0
	i += 1
otfile.close()
