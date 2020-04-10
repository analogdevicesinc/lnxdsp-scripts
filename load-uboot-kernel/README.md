# Setting Up Your Local Environment

## Prerequisites

You'll want the following installed locally:

* [Python](https://www.python.org/downloads/) 3.6 or greater

**Setup on Ubuntu 18.04:**
```bash
# install the basics
$ sudo apt install python3.7 python3-pip
```
# Usage #

```bash

# Just load with nfsboot, and no need to copy files
>sudo python3 LUK.py -b nfsboot -m adsp-sc584-ezkit --ipaddres 10.100.4.50 --serverip 10.100.4.174

# No need to update uboot and load with ramboot with providing deplyfolder
>sudo python3 LUK.py -b ramboot -m adsp-sc584-ezkit -f /tmp/deploy/images/adsp-sc584-ezkit

# CCES_HOME need to be set if update uboot, TODO, when openOCD repo is ready this should be change to OPENOCD_HOME
# Only update uboot, not laod kernel, 
>sudo CCES_HOME=/opt/analog/cces/${ccesVersion} python3 LUK.py -m adsp-sc584-ezkit --updateUboot -e 2000 --ipaddres 10.100.4.50 --serverip 10.100.4.174

# Update uboot and load with nfsboot with providing deplyfolder
>sudo CCES_HOME=/opt/analog/cces/${ccesVersion} python3 LUK.py -b nfsboot -m adsp-sc584-ezkit -f /tmp/deploy/images/adsp-sc584-ezkit/ --updateUboot -e 2000 --ipaddres 10.100.4.50 --serverip 10.100.4.174
```

### Help ###
``` bash    

Options:
  -h, --help            show this help message and exit

  [Options]:
    -m MACHINE, --machine=MACHINE
                          Specific the machine name,this a necessary option, e.g. adsp-sc589-ezkit
    -b BOOTTYPE, --bootType=BOOTTYPE
                          Specify the boot type like nfsboot,ramboot or sdcardboot
    -f DEPLOYFOLDER, --deployFolder=DEPLOYFOLDER
                          Specific the deploy folder to find the images that to be loaded
    -p COMPORT, --comPort=COMPORT
                          Specify the COM port connected to UART
    -e EMULATOR, --emulator=EMULATOR
                          Emulater used to connect with openOCD when update uboot, e.g. 1000, 2000
    --ipaddres=IPADDR   Provide IP address
    --serverip=SERVERIP   The IP address of the PC connected with board
    --updateUboot         Load the Uboot into flash with openOCD and GDB

```    
