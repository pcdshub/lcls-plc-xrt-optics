#!/bin/bash

source /cds/group/pcds/pyps/conda/pcds_conda

`pydm -m '{"YAXIS":"MR1L3:HOMS:MMS:YUP","XAXIS":"MR1L3:HOMS:MMS:XUP", "PITCH":"MR1L3:HOMS:MMS:PITCH", "MIRROR":"MR1L3"}' /reg/g/pcds/epics/ioc/xrt/HOMS_XRT/v3.0.0/homsScreens/mirrorScreen.py &`
