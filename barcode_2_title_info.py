#!/usr/bin/env python3


#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


# this script generates a friendly list of titles, authors (including editions) from a list of barcodes


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
df_rp_loeschen = pd.DataFrame(pd.read_csv(f"{filepath}/{files[ind]}", dtype=str, sep=delim))
df_rp_loeschen['barcode'] = df_rp_loeschen['barcode'].str.upper()


for i, el in enumerate(df_rp_loeschen['barcode']):
    req, get_item_info = api_request('get', el, 'json', 'items?item_barcode=')
    data = json.loads(get_item_info.content.decode(encoding='utf-8'))
    try:
        df_rp_loeschen.loc[i, 'call_number'] = data['holding_data']['call_number']
    except Exception as e:
        df_rp_loeschen.loc[i, 'call_number'] = e
    try:
        df_rp_loeschen.loc[i, 'title'] = data['bib_data']['title']
    except Exception as e:
        df_rp_loeschen.loc[i, 'title'] = e
    try:
        df_rp_loeschen.loc[i, 'author'] = data['bib_data']['author']
    except Exception as e:
        df_rp_loeschen.loc[i, 'author'] = e
    try:
        df_rp_loeschen.loc[i, 'isbn'] = data['bib_data']['isbn']
    except Exception as e:
        df_rp_loeschen.loc[i, 'isbn'] = e
    try:
        df_rp_loeschen.loc[i, 'complete_edition'] = data['bib_data']['complete_edition']
    except Exception as e:
        df_rp_loeschen.loc[i, 'complete_edition'] = e
    try:
        df_rp_loeschen.loc[i, 'date_of_publication'] = data['bib_data']['date_of_publication']
    except Exception as e:
        df_rp_loeschen.loc[i, 'date_of_publication'] = e

try:
    df_rp_loeschen.to_csv(f"{filepath}/output/title_list.csv", sep=delim)
except Exception as e:
    print(f"an error occurred: {e}")