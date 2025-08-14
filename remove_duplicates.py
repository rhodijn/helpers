#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


import csv, os, re


delim = ';'
files = []
filepath = 'files/'
liste = []
parts = []
searchterm = 'barcode'
set_1 = set()
set_2 = set()


files = os.listdir(filepath)

for el in files:
    if el.split('.')[-1] != 'csv':
        files.remove(el)

if len(files) > 1:
    print(f"Das Skript entfernt doppelte Titel aus 1 csv-Datei, {len(files)} gefunden.")
else:
    files.append(f"{files[0].split('.')[0]}_clnd.csv")
    print(f"Doppelte Einträge aus {files[0]} entfernt und in {files[1]}")