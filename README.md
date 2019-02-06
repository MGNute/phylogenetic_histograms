# PICAN-PI

This repository contains the code used in the paper "PICAN-PI: A Graphical Schema to Visualize Microbial Biodiversity" by Nute et al. It is a reference implementation of the PICAN-PI graph and some scripts that can be used in conjuction with the publicly available data on the Illinois Data Bank (IDB) (LINK) to reproduce the graphics used in that paper.


### Dependencies
This library depends on the following packages:
- DendroPy 4.0+
- PyCairo
- wxPython 4.0+ (only required if you want to use the GUI)
- OpenCV (animations code only)
- SEPP (uses SEPP output specifically, though this is not needed if you are using someone else's output)

This code has been tested primarily on Windows, although in some cases on Mac as well. Several parts of this code are pulled from another library which was tested on Linux as well. I would expect that it would work fine on both Mac and Linux too as long as cairo and dendropy import properly.

### Reference Data
In order to use this code you will need output from SEPP, at a minimum. It is helpful to have ready access to the alignment and tree that SEPP used along with some kind of meaningful annotation of the leaf nodes (in particular, a taxonomic annotation, but whatever labeling is of interest to you). The annotation must be tab-delimited with the names of the leaf nodes in the first columns, and labels in the following columns. See the example in the reference data on the IDB for guidance.

### Reproducing Graphics from Manuscript
The code required to reproduce the graphics in the PICAN-PI paper is contained in [run_examples_for_paper.py](blob/master/run_examples_for_paper.py)

### How to Use This Code
This code is meant to be a library that can be used within other scripts to generate these graphics in bulk and according to whatever customization the user desires. The files 'run_examples.py' and 'run_examples_for_paper.py' contain examples of scripts that incorporate the basic library to create large numbers of these graphics in bulk.

The core library for creating the PICAN-PI graphs includes the following modules, though in particular the first three:
- [art_manager.py](blob/master/art_manager.py): Includes an object called an ArtManager that does most of the interacting with cairo. This is a relatively lightweight object compared to the next one because it doesn't do any thinking about what should be drawn where, it just provides a bunch of helper methods and is the keeper of the cairo objects and output files.
- [data_controller.py](../blob/master/data_controller.py): This is the real monster of the repo. Declares an object called a DataManager that handles all the calculations and makes all the determinations about what should be drawn where. It also is responsible for keeping all references to data files and copies of data, including the reference data. 
    - Since this schema is very flexible and I have only been using it with SEPP output, I have tried to separate out a base DataManager object from an inheriting SeppJsonDataManager object. Since nothing else has been set up to inherit from DataManager, I may not have that abstraction quite right, but for this particular case it does work.
    - One big thing that the DataManager keeps track of is the reference tree (in the SEPP case, that's buried right in the SEPP JSON output, but in other cases is might have to seek this out). It currently loads and stores the tree as a DendroPy Tree() object, but at a lot of different it takes liberties with the DendroPy model by adding its own attributes. A better way to do that would be to store these in NumPy arrays since the reference tree topology is immutable for practical purposes. That has not been implemented here except for one unfinished function.
- [phylohist.py](../blob/master/phylohist.py): This module contains a few functions that are used both by the DataManager and by custom scripts, so a lot of them take an ArtManager and DataManager as arguments. Specifically though, most of these functions are related to drawing certain things, like the layout of the reference tree or the legend. As a result, they are prime for alteration and customization by the user, so they belong in a special place.
- [utilities.py](../blob/master/utilities.py): This module is just a bunch of miscelaneous utilities with scattered usage, but included for convenience.
- [settings.py](../blob/master/settings.py): This module has no actual code other than the declaration of a bunch of variables that double as settings. I know this is a frankly terrible way of managing user settings, but it was a minimally viable product for this library.

