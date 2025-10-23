#!/usr/bin/env python3


#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


# This script renames all files in a folder.


import os


filepath = 'files'


files = os.listdir(f"{filepath}/")
files = [f for f in files if os.path.isfile(f"{filepath}/{f}")]


for k, v in enumerate(files):
    parts = v.split('.')
    os.rename(f"{filepath}/{v}", f"{filepath}/file_{k}.{parts[-1]}")