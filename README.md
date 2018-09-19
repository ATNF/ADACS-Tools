# adacs-tools

This is a set of tools that I developed for testing primary beam models. It works as an extensive but relatively simple pipeline for processing simulated data using ASKAPSoft on a laptop. You can control the problem size to make it tractable.

It includes the following:

A couple of python tools that are used to generate input configuration files for the simulator:

1) primarybeam.py - A class used by the simular to mimic the power response of a telescope. This is used by the python script build_infiles.py - you should not have to change it.

2) build_infiles.py - This generates configuration files of the simulator to generate 2 overlapping ASKAP beams. There are a grid of point sources in the sky and they are visible by both beams. They are spread through the primary beam response. They are chosen to be in the middle of image pixels to minimise artefacts. There are so many of them though that deconvolution is required to get a nice image. THis is a pretty simple script - you could edit this to reduce the number of sources for example.

This by default generates a configuration file for 8 channels and 2 beams - so 16 files in total.

A script to run the simulator:

3) build_sim.sh

This needs to setup 2 directories for the simulation
