# PICAN-PI

This repository contains the code used in the paper "PICAN-PI: A Graphical Schema to Visualize Microbial Biodiversity" by Nute et al. It contains a reference implementation of the PICAN-PI graph and some scripts that can be used in conjuction with the publicly available data on the Illinois Data Bank (IDB) (LINK) to reproduce the graphics used in that paper.


### Dependencies
This library depends on the following packages:
- DendroPy
- Cairo
- wxPython 4.0+ (only required if you want to use the GUI)
- SEPP (uses SEPP output specifically, though this is not needed if you are using someone else's output)

This code has been tested primarily on Windows, although in some cases on Mac as well. Several parts of this code are pulled from another library which was tested on Linux as well. I would expect that it would work fine on both Mac and Linux too as long as cairo and dendropy import properly.

### Reference Data
In order to use this code you will need output from SEPP, at a minimum. It is helpful to have ready access to the alignment and tree that SEPP used along with some kind of meaningful annotation of the leaf nodes (in particular, a taxonomic annotation, but whatever labeling is of interest to you). The annotation must be tab-delimited with the names of the leaf nodes in the first columns, and labels in the following columns. See the example in the reference data on the IDB for guidance.

### How to Use This Code
The core library for creating the PICAN-PI graphs is contained in the two modules art_manager and data_controller.