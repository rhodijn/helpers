#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


import os


filepath = 'files'


files = os.listdir(filepath)

for k, v in enumerate(files):
    parts = v.split('.')
    os.rename(f"{filepath}/{v}", f"{filepath}/file_{k}.{parts[-1]}")