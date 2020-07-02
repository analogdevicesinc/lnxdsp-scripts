#########################################################################################
# Copyright (c), 2020 - Analog Devices Inc. All Rights Reserved. 
#########################################################################################
# File:
#   <LUK_Loader.py>
# Description:
#   LUK_Loader can Load uboot.ldr and linux Kernel to target board automatically
#   Use an independent class to be used when do test
#
#  Options machine, Boot Type, ipaddr, serverip are necessary when load kernel
#########################################################################################

import os,sys,re,time,optparse
import shutil
import subprocess
import signal
import serial
from config import OPENOCD_HOME, OPENOCD_CONFIG_PATH, OPENOCD_PATH, SERIAL_BAUDRATE, SERIAL_TIMEOUT
from LUK_Utility import copyFiles, LogFile, replaceMacros, COPY_DST_FOLDER

# Time is in seconds
SHORT_SLEEP_TIME = 2
WAIT_TIMEOUT = 5
UART_TIMEOUT = 3*60

# GDB related parameters
GDB_OPENOCD_DEFAULT_PORT = '3333'
GDB_DEFAULT_PATH = 'ARM/arm-none-eabi/bin/'
GDB_DEFAULT_BINARY = 'arm-none-eabi-gdb'
GDB_LOAD_UBOOT = 'u-boot-PROCESSOR'
GDB_ELF_FILE = 'init-PROCESSOR.elf'
GDB_ERROR_CMD = r'\^error,msg=(\".*\")'
GDB_PROMPT = '(gdb) \n'
GDB_SEND_CMDS = ['load %s'%GDB_ELF_FILE, 'c', 'Ctrl-c', 'load %s' %GDB_LOAD_UBOOT, 'c']

# BOOT commands for different boot type
DHCP_CMD = ['dhcp']
SET_IP = ['set serverip SERVER_IP', 'set ipaddr IP_ADDR']
BOOT_CMD = {
'update_uboot': ['run update'],
'nfsboot': ['run nfsboot'],
'ramboot': ['run ramboot'],
'sdcardboot': ['run sdcardboot']
}

UBOOT_LOAD_PASS_MSG = 'sc #'
KERNEL_LOAD_PASS_MSG = 'MACHINE login:'

LOADER_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(LOADER_ROOT)

OPENOCD_DEFAULT_BINARY = 'openocd'
OPENOCD_TARGET_CFG_FILE = {
    'sc58[4|9]':'adspsc58x.cfg',
    'sc573':'adspsc57x.cfg',
}

class UbootKernelLoader:

    def __init__( self, parameters):

        self.machine = parameters['machine'].lower()
        self.bootType = parameters['bootType'].lower()
        self.emulator = parameters['emulator']
        self.deployFolder = parameters['deployFolder']
        self.ipaddr = parameters['ipaddr']
        self.serverip = parameters['serverip']
        self.updateUboot = parameters['updateUboot']
        self.dhcp = parameters['dhcp']
        self.serial = serial.Serial()
        self.serial.port = parameters['comPort']
        self.serial.baudrate = SERIAL_BAUDRATE
        self.serial.timeout = SERIAL_TIMEOUT
        if self.serial.isOpen(): self.serial.close()
        self.data = ''
        self.openocdProcess = None
        self.gdbProcess = None
        self.logFile = None

    def copyImage( self ):
        copyFiles(self.bootType, self.machine, self.deployFolder, self.updateUboot)

    def connect( self ):
        if self.updateUboot:
            self.openOCDLog = LogFile( os.path.join( os.path.relpath( os.getcwd() ), 'OpenOCD.log' ) )
        if self.logFile:
            self.logFile.close()
        self.logFile = LogFile( os.path.join( os.path.relpath( os.getcwd() ), 'output.log' ) )

    def disConnect( self ):

        def terminateProcess(process):
            if process and process.poll() is None:
                process.terminate()
            time.sleep(SHORT_SLEEP_TIME)
            process = None

        if self.logFile:
            self.logFile.close()
        if self.updateUboot:
            self.openOCDLog.close()
        for process in (self.openocdProcess, self.gdbProcess):
            terminateProcess(process)

    def load(self,):
        pwCfg = os.path.join( LOADER_ROOT ,"PW_RESET.CFG")
        self.serial.open()
        if self.serial.isOpen():
            if self.emulator and self.updateUboot and ((self.ipaddr and self.serverip) or self.dhcp):
                # update uboot with openOCD and GDB
                self.loadOpenOCD()
                self.loadGDB()
            elif os.path.isfile(pwCfg):
                # handle the power cycle in automation testing when don't update the uboot
                self.logOutput( 'Power reset board with file %s.'%pwCfg, printout = True )
                with open( pwCfg, 'r' ) as f:
                    content = f.readlines()
                for line in content:
                    os.system(line)
            else:
                # handle the power cycle in manually when debugging
                input( "Please reset your board manually, and click KeyBoard enter in 5 seconds...")

            if self.bootType:
                # load kernel via serial port communication
                self.loadKernel()
            self.logOutput( self.data, True )
            self.serial.close()

    ##########################################################################
    # Helper Methods
    ##########################################################################
    def loadOpenOCD (self):
        # this need update once openocd has independent repo
        openOCDHome = OPENOCD_HOME
        if not openOCDHome:
            raise Exception( 'Failed to determine openOCD path. Has the OPENOCD_HOME environment variable been set correctly?' )
        # setup for openocd
        emulatorCfg = 'ice%s.cfg'%self.emulator
        configfile = ''
        for regex in OPENOCD_TARGET_CFG_FILE:
            if re.findall(regex, self.machine.split("-")[1]):
                configfile = OPENOCD_TARGET_CFG_FILE[regex]

        if configfile and emulatorCfg:
            self.logOutput(text = "Connecting board via openOCD", printout = True )
            self.openocdProcess = subprocess.Popen( 
                args = [ os.path.normpath( os.path.join( openOCDHome, OPENOCD_PATH, OPENOCD_DEFAULT_BINARY ) ),
                            '-f', 'interface/%s'%emulatorCfg,
                            '-f', 'target/%s'%configfile,
                            ],
                cwd = os.path.normpath( os.path.join( openOCDHome, OPENOCD_CONFIG_PATH ) ),
                stdout = self.openOCDLog.logFile,
                stderr = subprocess.STDOUT )
        else:
            raise RuntimeError( 'Cannot find debug configuration file or emulator configuration file ' )

    def loadGDB(self):
        # setup for GDB
        self.logOutput(text = "Debugging via GDB", printout = True )
        gdbPath = GDB_DEFAULT_PATH
        gdbBin = GDB_DEFAULT_BINARY
        self.gdbProcess = subprocess.Popen( 
            args = [ os.path.normpath( os.path.join( OPENOCD_HOME, gdbPath, gdbBin ) ), 
                    '-q', '--interpreter=mi2', '--nx', GDB_LOAD_UBOOT.replace("PROCESSOR", self.machine[5:])],
            cwd =  os.path.normpath(COPY_DST_FOLDER),
            stdin = subprocess.PIPE, 
            stdout =  subprocess.PIPE,
            stderr = subprocess.STDOUT )

        self.logOutput( self.read_until_prompt(), True )
        self.send_cmd_gdb( 'target remote :%s' %GDB_OPENOCD_DEFAULT_PORT )
        try:
            self.logOutput( self.read_until_prompt(), True )
        except:pass

        for cmd in replaceMacros([("PROCESSOR", self.machine[5:])], GDB_SEND_CMDS) :
            if cmd == 'Ctrl-c': 
                self.gdbProcess.send_signal(signal.SIGINT)
            else:
                self.send_cmd_gdb( cmd )
            self.logOutput( self.read_until_prompt(), True )
        time.sleep(SHORT_SLEEP_TIME)
        self.readSerialData()
        if self.data: self.serial.write(b'\n\n')
        updateUbootCmd = DHCP_CMD + BOOT_CMD['update_uboot'] if self.dhcp else \
            replaceMacros([('SERVER_IP', self.serverip), ('IP_ADDR', self.ipaddr)], SET_IP) + BOOT_CMD['update_uboot']
        for cmd in updateUbootCmd:
            self.writeDataToSerial( cmd )
        self.logOutput(text = "U-boot updated succuesfully", printout = True )

    def loadKernel(self):
        self.readSerialData()
        if self.data: 
            self.serial.write(b'\n\n')
            self.logOutput(text = "Go into U-boot succuesfully", printout = True )
        # check whether u-boot load successfully or not.
        time.sleep(SHORT_SLEEP_TIME)
        self.readSerialData()
        if UBOOT_LOAD_PASS_MSG in self.data:  
            for bt in BOOT_CMD:
                if bt == self.bootType:
                    # save the boot information, then auto boot will go into the correct boot type
                    self.writeDataToSerial( "setenv bootcmd %s"%BOOT_CMD[bt][0] )
                    for ip in replaceMacros([('SERVER_IP', self.serverip), ('IP_ADDR', self.ipaddr)], SET_IP):
                        self.writeDataToSerial( ip )
                    self.writeDataToSerial( "saveenv" )
                    for cmd in BOOT_CMD[bt]:
                        self.writeDataToSerial( cmd )
            startTime = time.time()
            endTime = time.time()
            bootKernelResultFlag = False
            while (endTime - startTime) < UART_TIMEOUT:
                self.readSerialData()
                if KERNEL_LOAD_PASS_MSG.replace('MACHINE', self.machine) in self.data: 
                    self.logOutput(text = "Load kernel successfully with %s" %self.bootType, printout = True )
                    bootKernelResultFlag = True
                    break
                endTime = time.time()
            if not bootKernelResultFlag:
                self.logOutput(text = "Load kernel failed, please check the log %s" %self.data, printout = True )
        else: 
            self.disConnect()
            raise Exception("Can not go into U-boot, please check manually.")

    def logOutput( self, text, raiseError = False, printout = False ):
        ''' write the given text to the output log '''
        # for brevity we omit any blank lines
        text = text.strip()
        if len( text ) > 0:
            lines = ['   ' + l.strip() for l in text.split( '\n' )]
            output = '\n'.join( lines )
            self.logFile.write( '\n' + output + '\n' )
            self.logFile.flush()
        # raise RuntimeError if there is error in GDB console output
        if printout:
            print(text)
        if raiseError:
            for s in text.split('\n'):
                error_match = re.match( GDB_ERROR_CMD, s)
                if error_match: raise RuntimeError( 'ERROR: %s' %error_match.group(1) )

    def read_until_prompt( self, process=None, message='', timeout=WAIT_TIMEOUT, timestamp=None):

        def checkTimeout(timeout=WAIT_TIMEOUT, timestamp=None):
            if timestamp:
                if time.time() - timestamp > timeout:
                    return True
            return False
        runTime = timestamp
        message = GDB_PROMPT if not message else message
        if process is None: process = self.gdbProcess 
        output = ''
        while(True):
            line = process.stdout.readline().decode('utf-8')
            output += line
            if timestamp and checkTimeout(timeout=WAIT_TIMEOUT, timestamp=runTime):
                return output
            else:
                if not line or line.startswith(message): 
                    return output

    def send_cmd_gdb(self, cmd):
        msg = '%s\n' %cmd
        self.gdbProcess.stdin.write( msg.encode('utf-8') )
        self.gdbProcess.stdin.flush()

    def readSerialData(self,):
        data=self.serial.readline()
        while self.serial.inWaiting():
            for i in range(0,6):
                data = data + self.serial.readline()
        self.data += data.decode('utf-8', errors="replace")

    def writeDataToSerial(self, cmd, timeout=5):
        # the serial write need time to flush
        msg = '%s\n' %cmd
        time.sleep(timeout)
        self.readSerialData()
        if self.data and (self.data.splitlines()[-1] != UBOOT_LOAD_PASS_MSG):
            self.serial.write('\n'.encode('utf-8'))
            time.sleep(timeout)

        self.serial.write(msg.encode('utf-8'))
