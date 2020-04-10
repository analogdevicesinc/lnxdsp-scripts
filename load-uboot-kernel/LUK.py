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
from LUK_Options import Options
from LUK_Loader import UbootKernelLoader

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

    parameters = {
                "bootType": options.getBootType(),
                "machine": options.getMachine(),
                "deployFolder": options.getDeployFolder(),
                "emulator": options.getEmulator(),
                "ipaddres": options.getIpaddres(),
                "serverip": options.getServerip(),
                "updateUboot": options.getUpdateUboot(),
                "comPort": options.getComPort()
                }
    loadUbootKernel = UbootKernelLoader(parameters)
    if options.getDeployFolder():
        loadUbootKernel.copyImage()
    loadUbootKernel.connect()
    loadUbootKernel.load()
    loadUbootKernel.disConnect()  
  
if __name__ == '__main__':
	main()        
