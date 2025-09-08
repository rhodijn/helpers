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


import json, os, requests
import pandas as pd
from dotenv import dotenv_values

barcodes = []
files = []
filepath = 'files'
secrets = dotenv_values('.env')


def api_request(method: str, value: str, frmt: str, par_1: str, par_2='') -> tuple:
    """
    perform an api request and return the answer

    parameters:
    method: str = api request method (GET, PUT, POST, ...)
    value: str = item id
    frmt: str = format (json, xml)
    param_1: str = api parameter 1
    param_2: str = api parameter 2

    returns:
    tuple = (req: str, response: requests.models.Response)
    """
    response = False

    if method == 'get':
        req = f"{secrets['API_URL']}{par_1}{value}{par_2}&apikey={secrets['API_KEY']}&format={frmt}"
        response = requests.get(req)

    return req, response


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


for i, el in enumerate(df_wae_loeschen['barcode']):
    req, get_iz_mmsid = api_request('get', el, 'json', 'items?item_barcode=')
    data = json.loads(get_iz_mmsid.content.decode(encoding='utf-8'))
    mmsid_iz = data['bib_data']['mms_id']
    df_wae_loeschen.loc[i, 'mms id'] = mmsid_iz

try:
    df_wae_loeschen.to_csv('files/output/wae_loeschen.csv', index=False, sep=';')
except Exception as e:
    print(f"an error occurred: {e}")