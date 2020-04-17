#########################################################################################
# Copyright (c), 2020 - Analog Devices Inc. All Rights Reserved. 
# This software is PROPRIETARY & CONFIDENTIAL to Analog Devices, Inc.
# and its licensors.
#########################################################################################
# File:
#   <LOAD_Options.py>
# Description:
#   Get all the options for load uboot, Kernel
#
#########################################################################################
import shlex
import optparse
from LUK_Utility import checkValidIp

class _Options():

    def set( self, args ):

        # create the parser
        parser = optparse.OptionParser()

        # add the options
        parser.add_option( '-b', '--bootType', dest='bootType', default='', help='Specify the boot type like nfsboot,ramboot or sdcardboot, you can change BOOTTYPE in config file', )
        parser.add_option( '-m', '--machine', help='Specify the machine name, e.g. adsp-sc589-ezkit, you can change MACHINE in config file', dest='machine', default='' )
        parser.add_option( '-f', '--deployFolder', help='Specify the deploy folder to find the images that to be loaded, you can change DEPLOY_FOLDER in config file', dest='deployFolder', default='' )
        parser.add_option( '-e', '--emulator', help='Emulator used to connect with openOCD, e.g. 1000, 2000, you can change EMULATOR in config file', dest='emulator', default='' )
        parser.add_option( '-p', '--comPort', help='Specify the COM port connected to UART, you can change COM_PORT in config file', dest='comPort', default='' )
        parser.add_option('--ipaddr', help='Board IP Address, you can change IP_ADDR in config file', dest='ipaddr', default='' )
        parser.add_option('--serverip', help='The IP address of the PC connected with board, you can change SERVER_IP in config file', dest='serverip', default='' )
        parser.add_option('--updateUboot', help='Load the Uboot into flash with openOCD and GDB, you can change UBOOT_UPDATE in config file', action='store_true', dest='updateUboot', default=None )

        options = parser.parse_args( args = args )[0]

        self._bootType = options.bootType
        self._machine = options.machine
        self._deployFolder = options.deployFolder
        self._emulator = options.emulator
        self._comPort = options.comPort
        self._ipaddr = options.ipaddr
        self._serverip = options.serverip
        self._updateUboot = options.updateUboot

    def getBootType( self ):
        return self._bootType

    def getMachine( self ):
        return self._machine

    def getDeployFolder( self ):
        return self._deployFolder

    def getEmulator( self ):
        return self._emulator

    def getComPort( self ):
        return self._comPort

    def getIpaddr( self ):
        if self._ipaddr: 
            if not checkValidIp(self._ipaddr):
                raise Exception("IP address %s is invalid." %self._ipaddr)
        return self._ipaddr

    def getServerip( self ):
        if self._serverip: 
            if not checkValidIp(self._serverip):
                raise Exception("Server IP address %s is invalid." %self._serverip)
        return self._serverip

    def getUpdateUboot( self ):
        return self._updateUboot    
          
_options = _Options()

# treat this as a singleton so that all modules get the same options
def Options():
    return _options
