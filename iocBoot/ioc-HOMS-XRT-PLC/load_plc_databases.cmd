# Total records: 4120
callbackSetQueueSize(10240)
dbLoadRecords("HOMS_XRT_PLC.db", "PORT=ASYN_PLC,PREFIX=PLC:XRT:HOMS:,IOCNAME=$(IOC),IOC=$(IOC)")
