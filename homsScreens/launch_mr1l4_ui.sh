#!/bin/bash

source /cds/group/pcds/pyps/conda/pcds_conda

`pydm -m '{"YAXIS":"MR1L4:HOMS:MMS:YUP","XAXIS":"MR1L4:HOMS:MMS:XUP", "PITCH":"MR1L4:HOMS:MMS:PITCH", "MIRROR":"MR1L4"}' /reg/g/pcds/epics/ioc/xrt/HOMS_XRT/latest/homsScreens/mirrorScreen.py &`
