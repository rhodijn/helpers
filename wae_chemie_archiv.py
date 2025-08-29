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
filepath = 'files/'
searchterm = 'signatur'
set_1 = set()
set_2 = set()
set_3 = set()


files = os.listdir(filepath)


for el in files:
    parts = el.split('.')
    if parts[-1] != 'csv':
        files.remove(el)

if len(files) != 2:
    print(f"Der Vergleich benötigt 2 csv-Dateien, {len(files)} gefunden.")
else:
    print(f"Vergleich von {files[0]} und {files[1]}")

    with open(filepath + files[0], encoding='utf-8-sig') as csv_file:
        reader = csv.reader(csv_file, delimiter=delim)
        hdr_0 = next(reader)
        for row in reader:
            el = ''.join(row[0].strip().split(' '))
            if not re.search(searchterm, el):
                set_1.add(el)

    with open(filepath + files[1], encoding='utf-8-sig') as csv_file:
        reader = csv.reader(csv_file, delimiter=delim)
        hdr_1 = next(reader)
        for row in reader:
            el = ''.join(row[0].strip().split(' '))
            if not re.search(searchterm, el):
                set_2.add(el)

    hdr = hdr_0

    for el in hdr_1:
        if el not in hdr:
            hdr.append(el)
    
    for el in range(len(hdr)):
        hdr[el] = hdr[el].lower()

    data.clear()
    data.append(hdr)

    with open(filepath + files[0], encoding='utf-8-sig') as csv_file:
        reader = csv.reader(csv_file, delimiter=delim)
        hdr_0 = next(reader)
        new_row = []
        for n, row in enumerate(reader):
            new_row.clear()
            for i in range(len(hdr)):
                new_row.append('')
            for k, v in enumerate(row):
                new_row[hdr.index(hdr_0[k].lower())] = ''.join(v.strip().split(' ')).lower()
            
            data.append(new_row)

    for i in range(10):
        print(data[i])
    
    '''
            if n != 0:
                new_row.clear()
                for i in range(len(hdr)):
                    new_row.append('')
                for k, v in enumerate(row):
                    new_row[hdr.index(hdr_0[k].lower())] = str(''.join(v.strip().split(' ')).lower())
                data.append(new_row)
    '''

    with open(f"{filepath}output/union.csv", 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerows(data)

    print(f"{len(set_1)} Einträge in: {files[0]}")
    print(f"{len(set_2)} Einträge in: {files[1]}")

    print(f"{len(set_1.union(set_2))} Einträge total in beiden Dateien")
    print(f"{len(set_1.intersection(set_2))} gemeinsame Einträge in beiden Dateien vorhanden")
    print(f"{len(set_1.difference(set_2))} Einträge ausschliesslich in {files[0]}")
    print(f"{len(set_2.difference(set_1))} Einträge ausschliesslich in {files[1]}")