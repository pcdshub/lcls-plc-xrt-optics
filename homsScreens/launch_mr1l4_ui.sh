#!/bin/bash

export PCDS_CONDA_VER=5.3.0
source /cds/group/pcds/pyps/conda/pcds_conda

`pydm --hide-menu-bar --hide-nav-bar -m '{"DISP_NAME":"MR1L4", "BASE_PV":"MR1L4:HOMS"}' /reg/g/pcds/epics/ioc/xrt/HOMS_XRT/latest/homsScreens/mirrorScreen.py &`
