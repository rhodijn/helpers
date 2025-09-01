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

barcode = []
files = []
filepath = 'files'
ind = None


files = os.listdir(f"{filepath}/")

for k, v in enumerate(files):
    parts = v.split('.')
    if parts[-1] == 'csv':
        ind = k

df_wae_c = pd.DataFrame(pd.read_csv(f"{filepath}/{files[ind]}", dtype=str, sep=';'))

df_wae_c['strichcode'] = df_wae_c['strichcode'].str.upper()

print(type(df_wae_c))

barcode.append(input('Bitte scannen: '))

behalten = df_wae_c['strichcode'].isin(barcode)

print(behalten)

if behalten[0]:
    print('behalten')
else:
    print('ausscheiden')