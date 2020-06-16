###########################################################################################
# Copyright (c), 2020 - Analog Devices Inc. All Rights Reserved. 
###########################################################################################
# File:
#   <config.py>
# Description:
#   Provide necessary configuration macros used in this tool, users can edit this when use
#
###########################################################################################

# OPTIONS Variables
MACHINE = 'adsp-sc589-ezkit'    #Specify the machine name
EMULATOR = '2000'               #Emulator used to connect with openOCD
SERVER_IP = '10.100.4.174'      #The IP address of the PC connected with board
IP_ADDR = '10.100.4.50'         #Board IP Address

BOOTTYPE = 'nfsboot'            #Specify the boot type like nfsboot,ramboot or sdcardboot
COM_PORT = '/dev/ttyUSB0'       #Specify the COM port connected to UART
DEPLOY_FOLDER = ''              #Specify the deploy folder to find the images that to be loaded
UBOOT_UPDATE = True             #Load the Uboot into flash with openOCD and GDB, the default is none
DHCP = False                    #Use dhcp to get the ipadd and serverip automatically, the default is false

# OpenOCD Related Parameters
OPENOCD_HOME = '/opt/analog/cces/2.9.2' # TODO this need change when we have openOCD repo
OPENOCD_CONFIG_PATH = 'ARM/openocd/share/openocd/scripts/'
OPENOCD_PATH = 'ARM/openocd/bin/'

# Serial Port Configuration
SERIAL_BAUDRATE= 57600
SERIAL_TIMEOUT = 1

# mount.cifs username and password
MOUNT_USERNAME = 'test'
MOUNT_PASSWORD = 'test'
