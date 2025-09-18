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
df_wae_loeschen['Barcode'] = df_wae_loeschen['Barcode'].str.upper()


for i, el in enumerate(df_wae_loeschen['Barcode']):
    req, get_iz_mmsid = api_request('get', el, 'json', 'items?item_barcode=')
    data = json.loads(get_iz_mmsid.content.decode(encoding='utf-8'))
    try:
        mmsid_iz = data['bib_data']['mms_id']
        df_wae_loeschen.loc[i, 'MMS ID'] = mmsid_iz
    except:
        df_wae_loeschen.loc[i, 'MMS ID'] = 'not found'

    req, get_nz_mmsid = api_request('get', mmsid_iz, 'json', 'bibs/', '?view=full&expand=p_avail')
    data = json.loads(get_nz_mmsid.content.decode(encoding='utf-8'))
    try:
        df_wae_loeschen.loc[i, 'Network Id'] = data['linked_record_id']['value']
    except:
        df_wae_loeschen.loc[i, 'Network Id'] = 'not found'

try:
    df_wae_loeschen.to_csv(f"{filepath}/output/wae_loeschen.csv", sep=delim)
except Exception as e:
    print(f"an error occurred: {e}")