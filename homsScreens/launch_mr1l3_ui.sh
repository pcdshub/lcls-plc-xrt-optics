#!/bin/bash

source /cds/group/pcds/pyps/conda/pcds_conda

#`pydm -m '{"YAXIS":"MR1L3:HOMS:MMS:YUP","XAXIS":"MR1L3:HOMS:MMS:XUP", "PITCH":"MR1L3:HOMS:MMS:PITCH", "MIRROR":"XRTM1 MR1L3"}' mirrorScreen.ui &`

typhos mr1l3_homs &
