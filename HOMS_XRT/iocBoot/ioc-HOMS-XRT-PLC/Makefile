IOC_TOP=/reg/g/pcds/epics/ioc/common/ads-ioc/0.3.1
IOC_INSTANCE_PATH := $(shell pwd)

# Set PRODUCTION_IOC to 1 to move from a testing to a production IOC:
PRODUCTION_IOC := 0

PROJECT_NAME := HOMS_XRT
PROJECT_PATH := ../../HOMS_XRT.tsproj
PLC := HOMS_XRT_PLC

PYTMC_OPTS := 
PREFIX := PLC:$(PLC)

# With two $$, as in $$(IOC) below, this will be expanded in the
# environment of st.cmd:
DB_PARAMETERS := 'PREFIX=$(PREFIX):,IOCNAME=$$(IOC),IOC=$$(IOC)'

include $(IOC_TOP)/iocBoot/templates/Makefile.base
