#!/usr/bin/env python3


#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


# this script find the mms ids to the items in a list of barcodes


import math, os
import pandas as pd


barcodes = []
files = []
filepath = 'files'


# scan folder and exclude subfolders
files = os.listdir(f"{filepath}/")
files = [f for f in files if os.path.isfile(f"{filepath}/{f}")]


# find the first csv-file in the folder
for k, v in enumerate(files):
    parts = v.split('.')
    if parts[-1] == 'csv':
        ind = k

print(files[ind])

# convert csv-file to dataframe and capitalize the barccode column
df_wae_loeschen = pd.DataFrame(pd.read_csv(f"{filepath}/{files[ind]}", dtype=str, sep=';'))
df_wae_loeschen['barcode'] = df_wae_loeschen['barcode'].str.upper()

print(len(df_wae_loeschen))

for i, el in enumerate(df_wae_loeschen['barcode']):
    print(el)

print(len(df_wae_loeschen))