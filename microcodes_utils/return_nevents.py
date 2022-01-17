#!usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 10∶25∶50 2021
@author: daniel

RETURNS THE NUMBER OF EVENTS STORED IN A DATA FILE wavesN.txt
"""

from microcodes_modules.CAENReader import readChannels

directory = input('Type name of directory where data is saved ')

READ = readChannels('DATA/'+directory,Vpp=2.0)
print('Number of events: ', READ.nevents())
