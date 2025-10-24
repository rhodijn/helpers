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

# improvement for next version: make three lists: keep, throw, not_found


"""
barcodes for testing

EM000006330349
EM000007999133
EM000007997722
"""


import csv, os
import pandas as pd
from playsound3 import playsound


barcodes = []
bc_keep = []
bc_throw = []
bc_not_found = []
files = []
filepath = 'resources/rp'
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
df_rp = pd.DataFrame(pd.read_csv(f"{filepath}/{files[ind]}", dtype=str, sep=';'))
df_rp['barcode'] = df_rp['barcode'].str.upper()


# print the welcome message
print(f"\n\t[{46 * '='}]\n\t[ {'Scan your items':<44} ]")
print(f"\t[{46 * ' '}]\n\t[ {'Use a barcode scanner to scan items,':<44} ]")
print(f"\t[ {'you will get acoustic and visual feedback.':<44} ]\n\t[{46 * ' '}]")
print(f"\t[{46 * ' '}]\n\t[ {str('File: ' + files[ind]):<44} ]")
print(f"\t[{46 * ' '}]\n\t[ {'version 1, by zolo@zhaw.ch':>44} ]\n\t[{46 * '='}]\n")


# the main loop of the script
while True:
    barcodes.append(input(f"scan item (or press 'q' to exit): "))
    if barcodes[-1] in ['Q', 'q', '']:
        # if the input is 'q'
        print(f"\n\t[{46 * '='}]\n\t[ {'goodbye':<44} ]\n\t[{46 * ' '}]")
        print(f"\t[ items to retain:  {len(bc_keep):<26} ]")
        print(f"\t[ items to deselect:  {len(bc_throw):<24} ]")
        print(f"\t[ items not found:  {len(bc_not_found):<26} ]\n\t[{46 * '='}]")
        break
    else:
        # the input is not 'q'
        df_scanned = df_rp[df_rp['barcode'].isin(barcodes)]
        if df_scanned[df_scanned['keep'].notna()].size > 0:
            # if the column 'hicr' is not empty => marked for retention
            if barcodes[-1] not in bc_keep:
                bc_keep.append(barcodes[-1])
            playsound(f"{soundpath}/success.mp3", block=False)
            print(f"\n\t\t\t\t[{22 * '='}]")
            print(f"\t\t\t\t[ {'KEEP!':<20} ]\n\t\t\t", end='')
        elif df_scanned[df_scanned['keep'].isna()].size > 0:
            # if the column 'hicr' is empty => not marked for retention
            if barcodes[-1] not in bc_throw:
                bc_throw.append(barcodes[-1])
            playsound(f"{soundpath}/error.mp3", block=False)
            print(f"\n\t[{22 * '='}]")
            print(f"\t[ {'THROW':<20} ]")
        else:
            # if the item's barcode is not in the spreadsheet
            if barcodes[-1] not in bc_not_found:
                bc_not_found.append(barcodes[-1])
            playsound(f"{soundpath}/warning.mp3", block=False)
            print(f"\n\t[{22 * '='}]")
            print(f"\t[ {'barcode not found':<20} ]")
    print(f"\t[{22 * '='}]\n")
    barcodes.pop()
    # catch an error (if barcodes are not correctly removed from list)
    if len(barcodes) != 0:
        print(f"\n\t[{22 * '='}]")
        print(f"\t[ {str('list error: ' + str(len(barcodes))):<20} ]")
        print(f"\t[{22 * '='}]\n")

# write log files
with open(f"{filepath}/log/retain.csv", 'w', newline='') as csv_log:
    csv_writer = csv.writer(csv_log, delimiter=';')
    for el in bc_keep:
        csv_writer.writerow(el)