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
import pandas as pd

barcodes = []
files = []
filepath = 'files'
ind = None

"""
Barcodes for Tests

04300003064054
04300003064053
04300003064031
EM000006516443
EM000006324055
04300003047949
"""

files = os.listdir(f"{filepath}/")

for k, v in enumerate(files):
    parts = v.split('.')
    if parts[-1] == 'csv':
        ind = k

df_wae_c = pd.DataFrame(pd.read_csv(f"{filepath}/{files[ind]}", dtype=str, sep=';'))

df_wae_c['strichcode'] = df_wae_c['strichcode'].str.upper()

print('\n\t[=========================]\n\t[ Archivbestand Chemie    ]')
print('\t[ version 1, by zolo      ]\n\t[=========================]\n')

while True:
    barcodes.append(input('scan item (or press \'q\' to exit): '))
    if barcodes[-1] == 'q':
        print('\n\t[===================]\n\t[ bye               ]\n\t[===================]\n')
        break
    else:
        df_scanned = df_wae_c[df_wae_c['strichcode'].isin(barcodes)]
        if df_scanned[df_scanned['hicr'].notna()].size > 0:
            print('\n\t\t\t\t[===================]')
            print('\t\t\t\t[ KEEP!             ]\n\t\t\t', end='')
        elif df_scanned[df_scanned['hicr'].isna()].size > 0:
            print('\n\t[===================]')
            print('\t[ THROW             ]')
        else:
            print('\n\t[===================]')
            print('\t[ BARCODE NOT FOUND ]')
    print('\t[===================]\n')
    barcodes.pop()