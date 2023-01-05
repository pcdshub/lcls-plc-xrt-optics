#!/bin/bash

export PCDS_CONDA_VER=5.3.0
source /cds/group/pcds/pyps/conda/pcds_conda

#typhos mr2l0_homs &
`pydm --hide-menu-bar --hide-nav-bar -m '{"BASE_PV":"MR2L0:HOMS"}' /reg/g/pcds/epics-dev/screens/pydm/offset_mirror_screens/latest/mirrorScreen.py &`
