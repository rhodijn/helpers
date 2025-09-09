#!/usr/bin/env python3


#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


# this script reads a csv-file and evaluates the info in a specific column
# the feedback when an item's barcode is scanned is whether or not to retain the item


"""
barcodes for testing

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
filepath = 'files/chemie'
ind = None
soundpath = 'sounds'


# scan folder and exclude subfolders
files = os.listdir(f"{filepath}/")
files = [f for f in files if os.path.isfile(f"{filepath}/{f}")]


# find the first csv-file in the folder
for k, v in enumerate(files):
    parts = v.split('.')
    if parts[-1] == 'csv':
        ind = k


# convert csv-file to dataframe and capitalize the barccode column
df_wae_c = pd.DataFrame(pd.read_csv(f"{filepath}/{files[ind]}", dtype=str, sep=';'))
df_wae_c['strichcode'] = df_wae_c['strichcode'].str.upper()

mixer.init()


# print the welcome message
print(f"\n\t[{46 * '='}]\n\t[ {'Scan your items':<44} ]")
print(f"\t[{46 * ' '}]\n\t[ {'Use a barcode scanner to scan items,':<44} ]")
print(f"\t[ {'you will get acoustic and visual feedback.':<44} ]\n\t[{46 * ' '}]")
print(f"\t[{46 * ' '}]\n\t[ {str('File: ' + files[ind]):<44} ]")
print(f"\t[{46 * ' '}]\n\t[ {'version 1, by zolo@zhaw.ch':>44} ]\n\t[{46 * '='}]\n")


# the main loop of the script
while True:
    barcodes.append(input(f"scan item (or press 'q' to exit): "))
    if barcodes[-1] == 'q':
        # if the input is 'q'
        mixer.quit()
        print(f"\n\t[{46 * '='}]\n\t[ {'goodbye':<44} ]\n\t[{46 * '='}]\n")
        break
    else:
        # the input is not 'q'
        df_scanned = df_wae_c[df_wae_c['strichcode'].isin(barcodes)]
        if df_scanned[df_scanned['hicr'].notna()].size > 0:
            # if the column 'hicr' is not empty => marked to retain
            plays = mixer.Sound(f"{soundpath}/success.mp3")
            plays.play()
            print(f"\n\t\t\t\t[{22 * '='}]")
            print(f"\t\t\t\t[ {'KEEP!':<20} ]\n\t\t\t", end='')
        elif df_scanned[df_scanned['hicr'].isna()].size > 0:
            # if the column 'hicr' is empty => not marked to retain
            plays = mixer.Sound(f"{soundpath}/error.mp3")
            plays.play()
            print(f"\n\t[{22 * '='}]")
            print(f"\t[ {'THROW':<20} ]")
        else:
            # if the item's barcode is not in the spreadsheet
            plays = mixer.Sound(f"{soundpath}/error.mp3")
            plays.play()
            print(f"\n\t[{22 * '='}]")
            print(f"\t[ {'barcode not found':<20} ]")
    print(f"\t[{22 * '='}]\n")
    barcodes.pop()
    # catch an error (if barcodes are not correctly removed from list)
    if len(barcodes) != 0:
        plays = mixer.Sound(f"{soundpath}/error.mp3")
        plays.play()
        print(f"\n\t[{22 * '='}]")
        print(f"\t[ {str('list error: ' + str(len(barcodes))):<20} ]")
        print(f"\t[{22 * '='}]\n")