#!/usr/bin/env python3


#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


"""
Barcodes for Testing

04300003064054
04300003064053
04300003064031
EM000006516443
EM000006324055
04300003047949
"""


from pygame import mixer
import os
import pandas as pd


barcodes = []
files = []
filepath = 'files'
soundpath = 'sounds'
ind = None


mixer.init()


files = os.listdir(f"{filepath}/")
files = [f for f in files if os.path.isfile(f"{filepath}/{f}")]


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
        mixer.quit()
        break
    else:
        df_scanned = df_wae_c[df_wae_c['strichcode'].isin(barcodes)]
        if df_scanned[df_scanned['hicr'].notna()].size > 0:
            plays = mixer.Sound(f"{soundpath}/success.mp3")
            plays.play()
            print('\n\t\t\t\t[===================]')
            print('\t\t\t\t[ KEEP!             ]\n\t\t\t', end='')
        elif df_scanned[df_scanned['hicr'].isna()].size > 0:
            plays = mixer.Sound(f"{soundpath}/error.mp3")
            plays.play()
            print('\n\t[===================]')
            print('\t[ THROW             ]')
        else:
            print('\n\t[===================]')
            print('\t[ barcode not found ]')
    print('\t[===================]\n')
    barcodes.pop()
    if len(barcodes) != 0:
        plays = mixer.Sound(f"{soundpath}/success.mp3")
        plays.play()
        print('\n\t[===================]')
        print(f"\t[ list error: {len(barcodes)}     ]")
        print('\t[===================]\n')