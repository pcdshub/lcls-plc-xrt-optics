#! /bin/bash

# Setup the common directory env variables
if [ -e /reg/g/pcds/pyps/config/common_dirs.sh ]; then
	source /reg/g/pcds/pyps/config/common_dirs.sh
else
	source /afs/slac/g/pcds/config/common_dirs.sh
fi

# Setup edm environment
source $SETUP_SITE_TOP/epicsenv-cur.sh

# Screen directory information
EDM_TOP=homs_overview.edl
SCREENS_TOP=/reg/g/pcds/epics/ioc/fee/homs/R1.3.9/homsScreens

pushd $SCREENS_TOP
# Launch the window
edm -x -eolc $EDM_TOP &
