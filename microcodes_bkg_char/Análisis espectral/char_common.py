#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 19:12:12 2021

@author: daniel
"""

"""
>>> # Demonstrate set operations on unique letters from two words
...
>>> a = set('abracadabra')
>>> b = set('alacazam')
>>> a                                  # unique letters in a
{'a', 'r', 'b', 'c', 'd'}
>>> a - b                              # letters in a but not in b
{'r', 'd', 'b'}
>>> a | b                              # letters in a or b or both
{'a', 'c', 'r', 'd', 'b', 'm', 'z', 'l'}
>>> a & b                              # letters in both a and b
{'a', 'c'}
>>> a ^ b                              # letters in a or b but not both
{'r', 'd', 'b', 'm', 'z', 'l'}
"""


import numpy as np
import csv

file = open('common_peaks.csv')
data = csv.reader(file)

F04_1 = []
F04_dip = []
F04_2 = []
F05_l = []
F05_h = []
F05_1 = []
F08_1 = []

for row in data:
    [f04_1,f04_dip,f04_2,f05_l,f05_h,f05_1,f08_1] = row
    if len(f04_1)>0: F04_1.append(float(f04_1))
    if len(f04_dip)>0: F04_dip.append(float(f04_dip))
    if len(f04_2)>0: F04_2.append(float(f04_2))
    if len(f05_l)>0: F05_l.append(float(f05_l))
    if len(f05_h)>0: F05_h.append(float(f05_h))
    if len(f05_1)>0: F05_1.append(float(f05_1))
    if len(f08_1)>0: F08_1.append(float(f08_1))

# Coincidences in the 3 samples from 11/04
coinc_full04 = set(F04_1) & set(F04_dip) & set(F04_2)
print('All coincidences at 11/04:')
print(sorted(coinc_full04))
print('')

# Coincidences in the 2 samples from antennas at 11/04
coinc_ant04 = set(F04_1) & set(F04_2)
print('Coincidences in antennas at 11/04:')
print(sorted(coinc_ant04))
print('')

# Elements at dipole but not antennas at 11/04
nocoinc_dip_ant04 = set(F04_dip) - set(coinc_ant04)
print('Elements at dipole but not antennas at 11/04:')
print(sorted(nocoinc_dip_ant04))
print('')

# Elements at antennas but not dipole at 11/04
nocoinc_ant_dip04 = set(coinc_ant04) - set(F04_dip)
print('Elements at antennas but not dipole at 11/04:')
print(sorted(nocoinc_ant_dip04))
print('')

# Elements at first antennas but not second at 11/04
nocoinc_ant1_ant204 = set(F04_1) - set(F04_2)
print('Elements at first antenna but not second at 11/04:')
print(sorted(nocoinc_ant1_ant204))
print('')

# Elements at second antennas but not first at 11/04
nocoinc_ant2_ant104 = set(F04_2) - set(F04_1)
print('Elements at second antenna but not first at 11/04:')
print(sorted(nocoinc_ant2_ant104))
print('')


print('')
# Coincidences in the 3 samples from 11/05
coinc_full05 = set(F05_l) & set(F05_h) & set(F05_1)
print('Elements in 3 antennas at 11/05:')
print(sorted(coinc_full05))
print('')

# Elements in first but not in second antennas at 11/05
nocoinc_antl_anth05 = set(F05_l) - set(F05_h)
print('Elements in first antennas but not in second at 11/05:')
print(sorted(nocoinc_antl_anth05))
print('')

# Elements in second but not in first 11/05
nocoinc_anth_antl05 = set(F05_h) - set(F05_l)
print('Elements in second antennas but not in first 11/05:')
print(sorted(nocoinc_anth_antl05))
print('')

# Elements in second but not in third antennas at 11/05
nocoinc_anth_ant105 = set(F05_h) - set(F05_1)
print('Elements in second antennas but not in third at 11/05:')
print(sorted(nocoinc_anth_ant105))
print('')

# Elements in second but not in first 11/05
nocoinc_ant1_anth05 = set(F05_1) - set(F05_h)
print('Elements in third antenna but not in second 11/05:')
print(sorted(nocoinc_ant1_anth05))
print('')


print('')
# Coincidences in antennas without filter and anyone of 11/04
# Remember that the 8 channels with no filter were no taken simultaneously!
allin_04 = set(F04_1) ^ set(F04_dip) ^ set(F04_2)
coinc_04_08 = set(allin_04) & set(F08_1)
print('Coincidences at 11/04 and 11/08:')
print(sorted(coinc_04_08))
print('')

# Elements at 11/08 but not at 11/04
nocoinc_08_04 = set(F08_1) - set(allin_04)
print('Elements at 11/08 but not at 11/04:')
print(sorted(nocoinc_08_04))
print('')

# Elements at 11/04 but not at 11/08
nocoinc_04_08 = set(allin_04) - set(F08_1)
print('Elements at 11/04 but not at 11/08:')
print(sorted(nocoinc_04_08))
print('')


print('')
# Coincidences in antennas without filter and anyone of 11/08
allin_05 = set(F05_l) ^ set(F05_h) ^ set(F05_1)
coinc_05_08 = set(allin_05) & set(F08_1)
print('Coincidences at 11/05 and 11/08:')
print(sorted(coinc_05_08))
print('')

# Elements at 11/08 but not at 11/05
nocoinc_08_05 = set(F08_1) - set(allin_05)
print('Elements at 11/08 but not at 11/05:')
print(sorted(nocoinc_08_05))
print('')

# Elements at 11/05 but not at 11/08
nocoinc_05_08 = set(allin_05) - set(F08_1)
print('Elements at 11/05 but not at 11/08:')
print(sorted(nocoinc_05_08))
print('')


print('')
# Coincidences in ALL measurements
coinc_all = set(F04_1) & set(F04_dip) & set(F04_2) & set(F05_l) & set(F05_h) & set(F05_1) & set(F08_1)
print('Coincidences in ALL measurements:')
print(sorted(coinc_all))
print('')