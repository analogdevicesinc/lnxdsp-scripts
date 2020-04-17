#########################################################################################
# Copyright (c), 2020 - Analog Devices Inc. All Rights Reserved. 
# This software is PROPRIETARY & CONFIDENTIAL to Analog Devices, Inc.
# and its licensors.
#########################################################################################
# File:
#   <LUK.py>
# Description:
#   LUK can Load Uboot and Kernel to target board automatically
#
#  Options machine, Boot Type, ipaddr, serverip are necessary when load kernel
#########################################################################################

import os,sys
from config import MACHINE, EMULATOR, BOOTTYPE, COM_PORT, SERVER_IP, IP_ADDR, UBOOT_UPDATE, DEPLOY_FOLDER
from LUK_Options import Options
from LUK_Loader import UbootKernelLoader
from LUK_Utility import checkValidIp

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT)

#------------------------------------------------------ 
# Main
#------------------------------------------------------ 
def main(args=sys.argv):
    cwd = os.path.dirname( __file__ )
    if not os.path.isabs( cwd ):
        cwd = os.path.join( os.getcwd(), cwd )
    os.chdir( os.path.dirname( cwd ) )

    options = Options()
    options.set( args )

    if not (checkValidIp(IP_ADDR) and checkValidIp(SERVER_IP)) :
            raise Exception("Provided IP address or server IP in config file is invalid, please check manually." )

    parameters = {
                "bootType": options.getBootType() if options.getBootType() else BOOTTYPE,
                "machine": options.getMachine() if options.getMachine() else MACHINE,
                "deployFolder": options.getDeployFolder() if options.getDeployFolder() else DEPLOY_FOLDER,
                "emulator": options.getEmulator() if options.getEmulator() else EMULATOR,
                "ipaddr": options.getIpaddr() if options.getIpaddr() else IP_ADDR,
                "serverip": options.getServerip() if options.getServerip() else SERVER_IP,
                "updateUboot": options.getUpdateUboot() if options.getUpdateUboot() else UBOOT_UPDATE,
                "comPort": options.getComPort() if options.getComPort() else COM_PORT
                }
    loadUbootKernel = UbootKernelLoader(parameters)
    if options.getDeployFolder():
        loadUbootKernel.copyImage()
    loadUbootKernel.connect()
    loadUbootKernel.load()
    loadUbootKernel.disConnect()  
  
if __name__ == '__main__':
	main()        
