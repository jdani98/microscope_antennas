#!/bin/bash

echo '**********************************************************************'
echo '***** EXECUTABLE TO CREATE 8 CH FULL CHARACTERIZATION OF SIGNALS *****'
echo '**********************************************************************'
echo ''
echo 'Introduce name of directory with data to analyze '
read dir
echo ''

echo '=================> Ch0'
python3 event_run.py $dir 0 0
python3 histo_run.py $dir 0
python3 psd2_run.py $dir 0
echo '=================> Ch1'
python3 event_run.py $dir 1 0
python3 histo_run.py $dir 1
python3 psd2_run.py $dir 1
echo '=================> Ch2'
python3 event_run.py $dir 2 0
python3 histo_run.py $dir 2
python3 psd2_run.py $dir 2
echo '=================> Ch3'
python3 event_run.py $dir 3 0
python3 histo_run.py $dir 3
python3 psd2_run.py $dir 3
echo '=================> Ch4'
python3 event_run.py $dir 4 0
python3 histo_run.py $dir 4
python3 psd2_run.py $dir 4
echo '=================> Ch5'
python3 event_run.py $dir 5 0
python3 histo_run.py $dir 5
python3 psd2_run.py $dir 5
echo '=================> Ch6'
python3 event_run.py $dir 6 0
python3 histo_run.py $dir 6
python3 psd2_run.py $dir 6
echo '=================> Ch7'
python3 event_run.py $dir 7 0
python3 histo_run.py $dir 7
python3 psd2_run.py $dir 7
