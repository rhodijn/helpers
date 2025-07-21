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
    with open(filepath + files[0]) as csv_liste_1:
        liste_reader = list(csv.reader(csv_liste_1, delimiter=delim))
        for el in enumerate(liste_reader[0]):
            if re.search(searchterm, el[1].lower()):
                i = el[0]
        for el in liste_reader:
            if not re.search(searchterm, el[i].lower()):
                set_1.add(el[i])

    with open(filepath + files[1]) as csv_liste_2:
        liste_reader = list(csv.reader(csv_liste_2, delimiter=delim))
        for el in enumerate(liste_reader[0]):
            if re.search(searchterm, el[1].lower()):
                i = el[0]
        for el in liste_reader:
            if not re.search(searchterm, el[i].lower()):
                set_2.add(el[i])

    for el in set_1:
        if el not in set_2:
            one_not_two.append(el)

    for el in set_2:
        if el not in set_1:
            one_not_two.append(el)

    print(f"{len(set_1)} einzigartige Elemente gefunden in: {files[0]}")
    print(f"{len(set_2)} einzigartige Elemente gefunden in: {files[1]}")

    if one_not_two:
        print(f"Nur in der ersten Liste vorhanden: {one_not_two}")
    else:
        print('Es gibt keine Elemente, die nur in der ersten Liste vorhanden sind.')

    if two_not_one:
        print(f"Nur in der zweiten Liste vorhanden: {two_not_one}")
    else:
        print('Es gibt keine Elemente, die nur in der zweiten Liste vorhanden sind.')