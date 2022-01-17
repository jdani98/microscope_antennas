# microscope_antennas
This repository contains all the software for the treatment of digital signals recorded in the MICROSCOPE Project [^footnote1] by the device of the antennas.

[^footnote1]:  Juan A. Garzón, _Atomic, Nuclear and Molecular Physics, Department of Particle Physics_, IGFAE (USC)<br/>
               John Xuna, _Cosmic Particles and Fundamental Physics researcher_, IGFAE (USC)<br/>
               José Daniel Viqueira Cao, _Cosmic Rays researcher_, IGFAE (USC) (creator of this repository)

Please **read** the instructions before dowloading and executing the software.

## How to download this repository and prepare it locally?
Press the green button to download the .zip and then unzip it in a local repo, or, copy the link and then type `git clone <link>` in a terminal.

Once cloned locally, an intermediate **step** is necessary to execute any program inside. Create in the main branch two directories: `DATA` and `OUTPUTS`.
With this step the programs are ready to be executed.

> 🚨 The software is ready to be executed in linux. Necessary to have installed `jupyter` and `python3`.

## Content
  - **`microcodes_modules`**: necessary python modules to make the rest of the programs run
    - `CAEN_Reader.py`: Contains classes to automatically read files from WaveDump
    - `auto_plots.py`: Contains classes to make easier the plot of histograms and computation of basic statistics
    - `events.py`: Defines a signal event (defined as the set of samples recorded by a trigger) as a class
    - `functions.py`: Defines several uncorrelated python functions, useful for different programs
  - **`microcodes_amp_filtering`**: jupyter programs used for filtering signals in amplitudes and try to detect individual pulses. Normally divide one event in time windows and compares the statistical parameters between them. The window of interest is that which is supposed to contain the pulse, as the trigger fall in it.
    - `counts_th_separated.ipynb`: counts over threshold in different windows + trend with scintillator voltage
    - `counts_th_separated_2.ipynb`: counts over threshold in different windows version 2 + trend with scintillator voltage
    - `counts_th_separated_sync.ipynb`: counts over threshold in different windows + channel summation + trend with scintillator voltage
    - `counts_th_separated_sync_2.ipynb`: counts over threshold in different windows + channel summation + trend with scintillator voltage
    - `max_diffs.ipynb`: differences of maxima in different windows + trend with scintillator voltage
    - `stats_search.ipynb`: statistical detection of peaks of radio signals
    - `std_scintillator_separated.ipynb`: square deviations for different windows
    - `std_scintillator_separated_2.ipynb`: square deviations for different windows version 2 + trend with scintillator voltage
    - `std_scintillator_separated_sync.ipynb`: square deviations for different windows + channel summation + trend with scintillator voltage
    - `std_search.ipynb`: statistical detection of peaks of radio signals
  - **`microcodes_bkg_char`**: mainly python programs to make the characterization of the background noise from the digitized signals.
As the computation of data requires some time, the characterization is usually done in two steps: a program `_run.py` saves into a csv file the results from one single channel and another one `_plot.py` takes the data of the 8 channels and displays it. The .py programs must be run in a linux terminal by the command `> python3 name.py [iev] [ich] dir`, with `iev` the number of event (optional), `ich` the number of channel (only for `_run.py`) and `dir` the name of the directory to read **in quotes**. Instructions inside each code. All the data are saved in `OUTPUTS` in a file called `fullchar.dat` inside a directory with the same name as data.
    - **`Análisis espectral`**: contains results of detected frequency peaks and two programs to analyze them
      - `char_common.py`: finds common and non-common peaks between different acquisitions
      - `spectrum_systematics`: finds periodicity of peaks
    - Pair `event...`: show one event both in time and frequency (Fourier transform) domain
    - Pair `histo...`: make the histogram of amplitudes from all the samples
    - Pair `psd2...`: compute the mean Power Spectral Density, its variation, its phase, and detects the peaks of frequency
    - Pair `psd24h...`: compute the mean PSD (and its variation and phase) in groups and then shows its evolution during time
    - `psd_plot.py`: display only the mean PSD
    - `psdcor_plot.py`: display the mean PSD correcting the attenuation due to the transmission line
    - `psddif_run.py`: compute the difference between two mean PSD
    - Pair `timesdist...`: compute the time distribution of events during time
    - `fullchar_autorun.sh`: execute in bash automatically `event_run.py`, `histo_run.py` and `psd2_run.py` to automatically save the full characterization of signals
  - **`microcodes_utils`**: several useful programs. Less sofisticated than previous ones. Description in each code.
