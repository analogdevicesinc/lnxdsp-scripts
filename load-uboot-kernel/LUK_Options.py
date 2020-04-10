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

class _Options():

    def set( self, args ):

        if '-@' in args:
            # handle the specified @file
            n = args.index( '-@' )
            atFile = args[n + 1]

            with open( atFile ) as f:
                opts = shlex.split( ' '.join( f.readlines() ), posix = False )
                args.remove( args[n] )  # remove the -@
                args.remove( args[n] )  # remove the filename
                args.extend( opts )
                # we recurse here so that we can nest -@ commands for convenience
                return self.set( args )

        # create the parser
        parser = optparse.OptionParser()

        # add the options
        parser.add_option( '-@', '-@', dest = 'file', action = 'store', default = None, help = 'Specifies a file from which options should be read' )
        parser.add_option( '-b', '--bootType', dest='bootType', default='', help='Specify the boot type like nfsboot,ramboot or sdcardboot', )
        parser.add_option( '-m', '--machine', help='Specific the machine name, e.g. adsp-sc589-ezkit', dest='machine', default='' )
        parser.add_option( '-f', '--deployFolder', help='Specific the deploy folder to find the images that to be loaded', dest='deployFolder', default='' )
        parser.add_option( '-e', '--emulator', help='Emulater used to connect with openOCD, e.g. 1000, 2000', dest='emulator', default='' )
        parser.add_option( '-p', '--comPort', help='Specify the COM port connected to UART', dest='comPort', default='/dev/ttyUSB0' )
        parser.add_option('--ipaddres', help='Board IP Address', dest='ipaddres', default='10.100.4.50' )
        parser.add_option('--serverip', help='The IP address of the PC connected with board', dest='serverip', default='10.100.4.174' )
        parser.add_option('--updateUboot', help='Load the Uboot into flash with openOCD and GDB', action='store_true', dest='updateUboot', default=False )

        options = parser.parse_args( args = args )[0]

        self._bootType = options.bootType
        self._machine = options.machine
        self._deployFolder = options.deployFolder
        self._emulator = options.emulator
        self._comPort = options.comPort
        self._ipaddres = options.ipaddres
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

    def getIpaddres( self ):
        return self._ipaddres

    def getServerip( self ):
        return self._serverip

    def getUpdateUboot( self ):
        return self._updateUboot    
          
_options = _Options()

# treat this as a singleton so that all modules get the same options
def Options():
    return _options
