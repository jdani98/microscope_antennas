# microscope_antennas
This repository contains all the software for the treatment of digital signals recorded in the MICROSCOPE Project [^footnote1] by the device of the antennas.

[^footnote1]:  Juan A. Garzón, _Atomic, Nuclear and Molecular Physics, Department of Particle Physics_, IGFAE (USC)<br/>
               John Xuna, _Cosmic Particles and Fundamental Physics researcher_, IGFAE (USC)<br/>
               José Daniel Viqueira Cao, _Cosmic Rays researcher_, IGFAE (USC)

Please **read** the instructions before dowloading and executing the software.

## How to download this repository and prepare it locally?
Press the green button to download the .zip and then unzip it in a local repo, or, copy the link and then type `git clone <link>` in a terminal.

Once cloned locally, an intermediate **step** is necessary to execute any program inside. Create in the main branch two directories: `DATA` and `OUTPUTS`.
With this step the programs are ready to be executed.

> WARNING. The software is ready to be executed in linux. Necessary to have installed `jupyter` and `python3`.

## Content
  - `microcodes_modules`: necessary python modules to make the rest of the programs run
    - `CAEN_Reader`: 
