IOC_TOP = /reg/g/pcds/epics/ioc/common/ads-ioc/R0.5.0

IOC_INSTANCE_PATH := $(shell pwd)

# Set PRODUCTION_IOC to 1 to move from a testing to a production IOC:
PRODUCTION_IOC := 1

PROJECT_NAME = plc-HOMS-XRT-PLC
PROJECT_PATH := ../../HOMS_XRT/HOMS_XRT.tsproj
PLC = HOMS_XRT_PLC

PYTMC_OPTS :=
PREFIX = PLC:XRT:HOMS

include $(IOC_TOP)/iocBoot/templates/Makefile.base
