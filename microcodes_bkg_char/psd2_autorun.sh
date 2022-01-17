#!/bin/bash

echo 'Introduce name of directory to read data from '
read in_dir

echo '=================> Ch0'
python3 data_for_complete_PSDs.py $in_dir 0
echo '=================> Ch1'
python3 data_for_complete_PSDs.py $in_dir 1
echo '=================> Ch2'
python3 data_for_complete_PSDs.py $in_dir 2
echo '=================> Ch3'
python3 data_for_complete_PSDs.py $in_dir 3
echo '=================> Ch4'
python3 data_for_complete_PSDs.py $in_dir 4
echo '=================> Ch5'
python3 data_for_complete_PSDs.py $in_dir 5
echo '=================> Ch6'
python3 data_for_complete_PSDs.py $in_dir 6
echo '=================> Ch7'
python3 data_for_complete_PSDs.py $in_dir 7
