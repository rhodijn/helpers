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


delim = ';'
files = []
filepath = 'files/'
liste = []
one_not_two = []
two_not_one = []
parts = []
searchterm = 'barcode'
set_1 = set()
set_2 = set()


files = os.listdir(filepath)

for el in files:
    parts = el.split('.')
    if parts[-1] != 'csv':
        files.remove(el)

if len(files) != 2:
    print(f"Der Vergleich benötigt 2 csv-Dateien, {len(files)} gefunden.")
else:
    print(f"Vergleich von {files[0]} und {files[1]}")
    with open(filepath + files[0]) as csv_liste_1:
        liste_reader = list(csv.reader(csv_liste_1, delimiter=delim))
        for el in liste_reader:
            if not re.search(searchterm, el[0].lower()):
                set_1.add(el[0])
        print(len(set_1))

    with open(filepath + files[1]) as csv_liste_2:
        liste_reader = list(csv.reader(csv_liste_2, delimiter=delim))
        for el in liste_reader:
            if not re.search(searchterm, el[0].lower()):
                set_2.add(el[0])
        print(len(set_2))

"""
    print(f"{len(set_1)} Einträge in: {files[0]}")
    print(f"{len(set_2)} Einträge in: {files[1]}")

    print(f"{len(one_not_two)} Einträge nur in: {files[0]}")
    print(f"{len(two_not_one)} Einträge nur in: {files[1]}")
"""