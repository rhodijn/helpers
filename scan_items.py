#!/usr/bin/env python3


#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


# This script reads a csv-file and evaluates the info in a specific column.
# The feedback when an item's barcode is scanned is whether or not to retain the item.


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


files = os.listdir(f"{filepath}/")
files = [f for f in files if os.path.isfile(f"{filepath}/{f}")]


for k, v in enumerate(files):
    parts = v.split('.')
    if parts[-1] == 'csv':
        ind = k

df_wae_c = pd.DataFrame(pd.read_csv(f"{filepath}/{files[ind]}", dtype=str, sep=';'))
df_wae_c['strichcode'] = df_wae_c['strichcode'].str.upper()

mixer.init()

# print the welcome message
print(f"\n\t[{46 * '='}]\n\t[ {'Archivbestand Chemie':<45}]")
print(f"\t[{46 * ' '}]\n\t[ {'Use a barcode scanner to scan items.':<45}]")
print(f"\t[ {'You will get acoustic and visual feedback.':<45}]\n\t[{46 * ' '}]")
print(f"\t[ {'Version 1, by zolo ':>45}]\n\t[{46 * '='}]\n")

while True:
    barcodes.append(input(f"scan item (or press 'q' to exit): "))
    if barcodes[-1] == 'q':
        # if the input is 'q'
        mixer.quit()
        print(f"\n\t[{46 * '='}]\n\t[ {'goodbye':<45}]\n\t[{46 * '='}]\n")
        break
    else:
        # if the input is not 'q'
        df_scanned = df_wae_c[df_wae_c['strichcode'].isin(barcodes)]
        if df_scanned[df_scanned['hicr'].notna()].size > 0:
            # if the column 'hicr' is not empty => marked to retain
            plays = mixer.Sound(f"{soundpath}/success.mp3")
            plays.play()
            print(f"\n\t\t\t\t[{22 * '='}]")
            print(f"\t\t\t\t[ {'KEEP!':<21}]\n\t\t\t", end='')
        elif df_scanned[df_scanned['hicr'].isna()].size > 0:
            # if the column 'hicr' is empty => not marked to retain
            plays = mixer.Sound(f"{soundpath}/error.mp3")
            plays.play()
            print(f"\n\t[{22 * '='}]")
            print(f"\t[ THROW{16 * ' '}]")
        else:
            # if the item's barcode is not in the spreadsheet
            print(f"\n\t[{22 * '='}]")
            print(f"\t[ {'barcode not found':<21}]")
    print(f"\t[{22 * '='}]\n")
    barcodes.pop()
    if len(barcodes) != 0:
        plays = mixer.Sound(f"{soundpath}/error.mp3")
        plays.play()
        print(f"\n\t[{22 * '='}]")
        print(f"\t[ list error: {len(barcodes):<9}]")
        print(f"\t[{22 * '='}]\n")