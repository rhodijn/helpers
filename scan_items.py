#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################

# This script compares two csv-files and reports the differences.


import csv, os, re
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

while True:
    barcodes.append(input('scan items (\'q\' to exit): '))
    if barcodes[-1] == 'q':
        barcodes.pop()
        break

df_scanned = df_wae_c[df_wae_c['strichcode'].isin(barcodes)]

df_deselection = df_scanned[df_scanned['hicr'].isna()]
df_retention = df_scanned[df_scanned['hicr'].notna()]

print(f"books to keep:\n{df_retention}")
print(f"book to throw:\n{df_deselection}")