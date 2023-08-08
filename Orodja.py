import os
import csv

def ime_datoteke(st_strani):
    return f"Rabljena-plovila-{st_strani + 1}.html"

def izloci_gnezdene_podatke(barke):
    kategorije = []

    for barka in barke:
        for kategorija in barka.pop('kategorija'):
            kategorije.append({'id': barka['id'], 'kategorija': kategorija})

    kategorije.sort(key=lambda kategorija: (kategorija['id'], kategorija['kategorija']))

    return kategorije

def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8', newline='') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        writer.writerows(slovarji)