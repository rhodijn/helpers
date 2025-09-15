#!/usr/bin/env python3


#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


# this script finds the mms ids to the items in a list of barcodes


import json, os
import pandas as pd

from modules.apihandler import *


barcodes = []
delim = ';'
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

print(f"File: {files[ind]}")

# generate datafrome from csv-file, capitalize the barccode column
df_wae_loeschen = pd.DataFrame(pd.read_csv(f"{filepath}/{files[ind]}", dtype=str, sep=delim))
df_wae_loeschen['barcode'] = df_wae_loeschen['barcode'].str.upper()


for i, el in enumerate(df_wae_loeschen['barcode']):
    req, get_iz_mmsid = api_request('get', el, 'json', 'items?item_barcode=')
    data = json.loads(get_iz_mmsid.content.decode(encoding='utf-8'))
    try:
        mmsid_iz = data['bib_data']['mms_id']
        df_wae_loeschen.loc[i, 'mms id'] = mmsid_iz
    except Exception as e:
        df_wae_loeschen.loc[i, 'mms id'] = e

try:
    df_wae_loeschen.to_csv(f"{filepath}/output/wae_loeschen.csv", sep=delim)
except Exception as e:
    print(f"an error occurred: {e}")