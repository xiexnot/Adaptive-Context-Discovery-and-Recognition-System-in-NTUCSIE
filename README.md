#Adaptive Context Discovery and Recognition System in NTUCSIE

##Introduction

This is Adaptive Context Discovery and Recognition System from NTU CSIE. It's for my master thesis of Computer Science and Information Engineering.

This project has been upgraded based on proposed work [MARCS](http://ccc.ntu.edu.tw/research/projectinfo/marcs) and [M-CHESS](http://ccc.ntu.edu.tw/newsletters/m-chess-m2m-based-context-aware-home-energy-saving-system?language=en) in [Intel-NTU Center](http://ccc.ntu.edu.tw/). Thank you for the support from Distinguished Professor Li-Chen Fu and Dr.Chao-Lin Wu.

After the system has been completed, this github project will become private. And only one public and empty project will be left.



## Overview

- Activity Discovery Engine: MARCS_v2015.py

- Activity Recognition Engine (with Novelty Detection): MARCS_Recognition.py

- Activity Adaptation Engine: MARCS_Adaptation.py

- Addition Tools: pca.py, AP.py, tools.py

  ​

## Activity Discovery Engine

### MARCS_v2015

Configure Input: BL313\_full\_0.9_0.json

Parameters: dataset_filename, eigenvalue_sum_threshold, Pinit, eigenvalue_filename, eigenvector_filename, cluster_filename

Algorithm : Density-enhanced Affinity Propagation

Hints: Reference [Nonparametric Discovery of Contexts and Preferences in Smart Home Environments](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=7379623&tag=1)











