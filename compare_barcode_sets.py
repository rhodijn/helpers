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


data = []
delim = ';'
files = []
filepath = 'files'
searchterm = 'barcode'
set_1 = set()
set_2 = set()
set_3 = set()


files = os.listdir(f"{filepath}/")
files = [f for f in files if os.path.isfile(f"{filepath}/{f}")]


for el in files:
    parts = el.split('.')
    if parts[-1] != 'csv':
        files.remove(el)

if len(files) != 2:
    print(f"Der Vergleich benötigt 2 csv-Dateien, {len(files)} gefunden.")
else:
    print(f"Vergleich von {files[0]} und {files[1]}")

    with open(f"{filepath}/{files[0]}") as csv_file:
        reader = csv.reader(csv_file, delimiter=delim)
        for el in reader:
            if not re.search(searchterm, el[0].lower()):
                set_1.add(el[0])

    with open(f"{filepath}/{files[1]}") as csv_file:
        reader = csv.reader(csv_file, delimiter=delim)
        for el in reader:
            if not re.search(searchterm, el[0].lower()):
                set_2.add(el[0])

    data.clear()
    data.append(['barcode'])
    for element in set_1.union(set_2):
        data.append([element])

    with open(f"{filepath}/output/union.csv", 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerows(data)

    data.clear()
    data.append(['barcode'])
    for element in set_1.difference(set_2):
        data.append([element])

    with open(f"{filepath}/output/only_{files[0]}", 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerows(data)

    print(f"{len(set_1)} Einträge in: {files[0]}")
    print(f"{len(set_2)} Einträge in: {files[1]}")

    print(f"{len(set_1.union(set_2))} Einträge total in beiden Dateien")
    print(f"{len(set_1.intersection(set_2))} gemeinsame Einträge in beiden Dateien vorhanden")
    print(f"{len(set_1.difference(set_2))} Einträge ausschliesslich in {files[0]}")
    print(f"{len(set_2.difference(set_1))} Einträge ausschliesslich in {files[1]}")