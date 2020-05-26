# Setting Up Your Local Environment

**Setup on Ubuntu 18.04:**
```bash
# install the basics
$ source setup-load-env.sh
```
# Usage #

This tool will parse the macros in config.py file firstly, then check options like -m -b 

### Method 1: Update config.py file(for manual) ###

User just need to update the config.py file then run LUK.py, this is a better choice when user want to load manually.
```bash
# Update config.py file for the Macros you want to change like BOOTTYPE, EMULATOR,COM_PORT, then run
sudo python3 LUK.py
```

### Method 2: Change Macros via options(for automation) ###

Options from user have higher priority, when both options specified and macros in config.py, the tool will use options 
and keep the config.py no change, this is a better choice when user want to load in automation testing.
```bash
# Just load with nfsboot, and no need to copy files
>sudo python3 LUK.py -b nfsboot -m adsp-sc584-ezkit --ipaddr 10.100.4.50 --serverip 10.100.4.174

# No need to update uboot and load with ramboot with providing deploy folder
>sudo python3 LUK.py -b ramboot -m adsp-sc584-ezkit -f /tmp/deploy/images/adsp-sc584-ezkit

# Only update uboot, not load kernel, 
>sudo python3 LUK.py -m adsp-sc584-ezkit --updateUboot -e 2000 --ipaddr 10.100.4.50 --serverip 10.100.4.174

# Update uboot and load with nfsboot with providing deploy folder
>sudo python3 LUK.py -b nfsboot -m adsp-sc584-ezkit -f /tmp/deploy/images/adsp-sc584-ezkit/ --updateUboot -e 2000 --ipaddr 10.100.4.50 --serverip 10.100.4.174

# Update uboot and load with nfsboot with providing deploy folder using dhcp
>sudo python3 LUK.py -b nfsboot -m adsp-sc584-ezkit -f /tmp/deploy/images/adsp-sc584-ezkit/ --updateUboot -e 2000 --dhcp
```

### Help ###

Options just provide the necesssary macros that should be changed according to different situations.

``` bash    
Options:
  -h, --help            show this help message and exit

  [Options]:
    -m MACHINE, --machine=MACHINE
                          Specify the machine name, e.g. adsp-sc589-ezkit, you can change MACHINE in config file
    -b BOOTTYPE, --bootType=BOOTTYPE
                          Specify the boot type like nfsboot,ramboot or sdcardboot, you can change BOOTTYPE in config file
    -f DEPLOY_FOLDER, --deployFolder=DEPLOY_FOLDER
                          Specify the deploy folder to find the images that to be loaded, you can change DEPLOY_FOLDER in config file
    -p COM_PORT, --comPort=COM_PORT
                          Specify the COM port connected to UART, you can change COM_PORT in config file
    -e EMULATOR, --emulator=EMULATOR
                          Specify the emulator to connect with openOCD, e.g. 1000, 2000, you can change EMULATOR in config file
    --ipaddr=IP_ADDR      Board IP Address, you can change IP_ADDR in config file
    --serverip=SERVER_IP  The IP address of the PC connected with board, you can change SERVER_IP in config file
    --updateUboot         Load the Uboot into flash with openOCD and GDB, the default value is true, you can change UBOOT_UPDATE in config file
    --dhcp                Use dhcp to get the ipadd and serverip automatically, the default is false, you can change DHCP in config file

```    
