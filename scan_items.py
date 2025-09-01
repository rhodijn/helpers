#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


import os, winsound
import pandas as pd

barcodes = []
files = []
filepath = 'files'
ind = None

"""
Barcodes for Testing

04300003064054
04300003064053
04300003064031
EM000006516443
EM000006324055
04300003047949
"""

def play_sound(freq):
    winsound.Beep(freq, 300)

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
        print('\n\t[===================]\n\t[ goodbye           ]\n\t[===================]\n')
        break
    else:
        df_scanned = df_wae_c[df_wae_c['strichcode'].isin(barcodes)]
        if df_scanned[df_scanned['hicr'].notna()].size > 0:
            play_sound(1760)
            print('\n\t\t\t\t[===================]')
            print('\t\t\t\t[ KEEP!             ]\n\t\t\t', end='')
        elif df_scanned[df_scanned['hicr'].isna()].size > 0:
            play_sound(880)
            print('\n\t[===================]')
            print('\t[ THROW             ]')
        else:
            print('\n\t[===================]')
            print('\t[ barcode not found ]')
    print('\t[===================]\n')
    barcodes.pop()
    if len(barcodes) != 0:
        print('\n\t[===================]')
        print(f"\t[ list error: {len(barcodes)}     ]")
        print('\t[===================]\n')