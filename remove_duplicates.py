#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################

# This script removes ducplicates from a csv column and saves the list to a new csv-file.


import csv, os, re


delim = ';'
files = []
filepath = 'files/'
liste = []
parts = []
searchterm = 'barcode'
mms_id_set = set()
mms_id_list = []


files = os.listdir(filepath)

for el in files:
    if el.split('.')[-1] != 'csv':
        files.remove(el)

if len(files) > 1:
    print(f"Das Skript entfernt doppelte Titel aus 1 csv-Datei, {len(files)} gefunden.")
else:
    files.append(f"{files[0].split('.')[0]}_CLEANED.csv")
    print(f"Doppelte Einträge aus {files[0]} entfernt und in {files[1]}")

    with open(filepath + files[0]) as csv_liste:
        liste_reader = list(csv.reader(csv_liste, delimiter=delim))
        for k, v in enumerate(liste_reader[0]):
            if re.search(searchterm, v.lower()):
                break
        for el in liste_reader:
            if not re.search(searchterm, el[k].lower()):
                mms_id_set.add(el[k])

    mms_id_list = list(mms_id_set)

    with open(filepath + files[1], 'w', newline='') as file:
        writer = csv.writer(file)

    # Write each element of the list as a row in the CSV file
        for item in mms_id_list:
            writer.writerow([item])

    print(f"Set has been saved to {files[1]}")