#########################################################################################
# Copyright (c), 2020 - Analog Devices Inc. All Rights Reserved. 
# This software is PROPRIETARY & CONFIDENTIAL to Analog Devices, Inc.
# and its licensors.
#########################################################################################
# File:
#   <LUK_Utility.py>
# Description:
#   LUK_Utility provide the utility functions,class 
#
#########################################################################################

import os,re,sys, shutil,serial
from io import BytesIO as StringIO
import threading
import importlib
try:
    importlib.import_module('easyprocess')
except ImportError as e:
    os.system("%s -m pip install %s"%(sys.executable, 'easyprocess'))
from easyprocess import EasyProcess

# Utility related parameters when do image copy
IMAGE_TYPES = ['adsp-sc5xx-full', 'adsp-sc5xx-minimal', 'adsp-sc5xx-ramdisk'] 
COPY_DST_FOLDER = '/tftpboot'
NFS_TAR_FILE_POSTFIX = '.tar.xz'
NFS_DST_FOLDER= '/romfs'
NFS_CP_CMD_LIST = ["sudo rm -rf NFSFOLDER", "sudo mkdir NFSFOLDER", "sudo chmod 777 NFSFOLDER", "tar -xvf NFS_SRC_TAR_FILE -C NFSFOLDER" ]
RAMDISK_FILE_POSTFIX = '.cpio.xz.u-boot'
RAMDISK_FILE_NAME = 'ramdisk.cpio.xz.u-boot'
UBOOT_FILE_LIST = ['u-boot-PROCESSOR', 'u-boot-PROCESSOR.ldr','init-PROCESSOR.elf']
Z_IMAGE = 'zImage'
DTB_POSTFIX = '.dtb'

	
def copyFiles(bootType, machine, deployFolder, updateUboot = True):

    fileList = []
    os.environ[ 'tftp' ] = COPY_DST_FOLDER
    processor = machine[5:]

    if updateUboot:
        fileList += replaceMacros([("PROCESSOR", processor)], UBOOT_FILE_LIST)

    if bootType.lower() in ("nfsboot", "ramboot") :
        fileList += [ Z_IMAGE, processor + DTB_POSTFIX ]
        tarFile = ''
        ramdiskFile = ''
        if deployFolder.startswith('//'):
            mount = '/mnt/shared'
            unmountCmd = ['umount', '-l', mount]
            if not os.path.exists(mount):
                os.mkdir(mount)
            if os.path.ismount(mount):
                EasyProcess(unmountCmd).call(timeout=10)
            p = EasyProcess(['mount','-t', 'cifs', deployFolder,mount, '-o', 'user=testlab2,password=Labrat1' ]).call(timeout=10)
            if 'mount error' in p.stderr:
                p = EasyProcess(['mount','-t', 'cifs', deployFolder,mount, '-o', 'user=testlab2,password=Labrat1,vers=3.0' ])
            if p.return_code not in (0, 8192, 256):
                raise Exception(f"Failed to mount the shared folder {deployFolder}:{p.stderr}")
            deployFolder = mount
        for (roots, dirs, files ) in os.walk( deployFolder ):
            for f in files:
                for image in IMAGE_TYPES:
                    targetTarFile = "%s-%s%s" %(image, machine, NFS_TAR_FILE_POSTFIX)
                    targetRamdiskFile = "%s-%s%s" %(image, machine, RAMDISK_FILE_POSTFIX)
                    if f == targetTarFile: 
                        tarFile = targetTarFile
                    elif f == targetRamdiskFile: 
                        ramdiskFile = RAMDISK_FILE_NAME
                        shutil.copyfile(os.path.join(deployFolder, targetRamdiskFile), os.path.join(deployFolder, RAMDISK_FILE_NAME))

        if bootType == "nfsboot":
            if tarFile == '':
                raise Exception("Can't find the NFS tar file")
            os.environ[ 'rootfs' ] = NFS_DST_FOLDER
            nfsTarFile = os.path.join(deployFolder, tarFile)
            cmdList = replaceMacros([('NFSFOLDER', NFS_DST_FOLDER), ('NFS_SRC_TAR_FILE', nfsTarFile)], NFS_CP_CMD_LIST)
            for cmd in cmdList: 
                os.system(cmd)

        if bootType == "ramboot":
            if ramdiskFile == '':
                raise Exception("Can't find the ramdisk file")
            fileList.append(ramdiskFile)

    if bootType == "sdcardboot":
            pass # TODO, will add more boot type later
    # cleanup the COPY_DST_FOLDER like /tftpboot before copy files
    if os.path.exists(COPY_DST_FOLDER):
        for f in os.listdir( COPY_DST_FOLDER ):
            src = os.path.join( COPY_DST_FOLDER, f )
            if os.path.isfile( src ):
                os.remove( src )
    else:
        os.makedirs( COPY_DST_FOLDER )
    for file in fileList:
        fileDir = os.path.join(deployFolder, file)
        if os.path.isfile(fileDir):
            shutil.copyfile(fileDir, os.path.join(COPY_DST_FOLDER, file))
        else:
            raise Exception("Can't copy due to the %s doesn't exist in %s" %(fileDir, deployFolder) )

def replaceMacros(macros, cmdList):
    # replace the uppercase macros to real data 
    updatedList = []
    for line in cmdList:
        for macro in macros:
            line = line.replace(macro[0], macro[1])
            updatedList.append( line )

    return updatedList 

def checkValidIp (Ip):
    regex = r'''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''
    if(re.search(regex, Ip)):  
        return True     
    else:  
        return False

class LogFile:

    def __init__( self, fileName ):
        self.buffer = StringIO()
        self.logFile = open( fileName, 'w' )

    def getText( self ):
        return self.buffer.getvalue()

    def close( self ):
        self.buffer.close()
        self.logFile.close()

    def write( self, s ):
        self.buffer.write( s.encode('utf-8') )
        self.logFile.write( s )

    def flush( self ):
        self.logFile.flush()

