#!/bin/bash

source /cds/group/pcds/pyps/conda/pcds_conda

`pydm -m '{"YAXIS":"MR2L3:HOMS:MMS:YUP","XAXIS":"MR2L3:HOMS:MMS:XUP", "PITCH":"MR2L3:HOMS:MMS:PITCH", "MIRROR":"MR2L3"}' /reg/g/pcds/epics/ioc/xrt/HOMS_XRT/latest/homsScreens/mirrorScreen.py &`
