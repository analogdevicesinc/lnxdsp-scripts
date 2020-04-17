#########################################################################################
# Copyright (c), 2020 - Analog Devices Inc. All Rights Reserved. 
# This software is PROPRIETARY & CONFIDENTIAL to Analog Devices, Inc.
# and its licensors.
#########################################################################################
# File:
#   <setup-load-env.sh>
# Description:
#   setup-load-env setup the virtual environment for users to run in virtual environment
#   This won't pollute users' python envrionment.
#
#########################################################################################

sudo apt install python3 python3-venv python3-pip -y
python3 -m venv .venv
source ./.venv/bin/activate
pip3 install pyserial
