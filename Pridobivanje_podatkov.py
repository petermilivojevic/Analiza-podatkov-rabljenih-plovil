import re
import requests
import csv
import os
import numpy as np
import pandas as pd

vzorec = re.compile(
    r'<p class="blurb__title-header">(?P<kategorija>[^<]*)</p>'
    r'<h3 class="blurb__title">.*/(?P<id>\d+)/" title="'
    r'.*>(?P<ime>[^<]*)</a></h3>'
    r'.*<ul class="blurb__facts"><li class="blurb__fact"><span class="blurb__value">(?P<dolzina>[\d\.]*)'
    r' x (?P<sirina>[\d\.]*) m</span>.*\n'
    r'<li class="blurb__fact">(.*|.*\n.*)(?!<li class="blurb__fact l-hide--lg-u">)li class="blurb__fact l-hide--lg-u">'
    r'<span class="blurb__value">(?P<leto>[^<]*)</span>'
    r'.*<p class="blurb__location">(?P<lokacija>[^<]*)'
    r'.*<p class="blurb__price">[^\d]*(?P<cena>[\d\.]*)[^<]*'
    r'.*<ul class="blurb__description"><li>(?P<uporabljenost>[^<]*)'
)

def izloci_podatke_bark(blok):
    barka = vzorec.search(blok).groupdict()
    barka['id'] = int(barka['id'])
    barka['ime'] = barka['ime']
    barka['kategorija']  = barka['kategorija'].strip().split(', ')
    barka['dolzina'] = float(barka['dolzina'])
    barka['sirina'] =float(barka['sirina'])
    barka['leto'] = int(barka['leto'])
    barka['uporabljenost'] = barka['uporabljenost']
    barka['cena'] = barka['cena'].replace('.', '')
    barka['lokacija'] = barka['lokacija']
    return barka

def ime_datoteke(st_strani):
    return f"Rabljena-plovila-{st_strani + 1}.html"

st_strani = 58

for i in range(st_strani):
    if i == 0:
        url = (
        'https://www.boat24.com/en/secondhandboats/?src=&cat=&whr=EUR&prs_min=&prs_max=&lge_min=1&lge_max=999&bre_min=1&bre_max=999&rgo%5B%5D=51&rgo%5B%5D=31&jhr_min=1&jhr_max=2024&sort=lgedesc'
    )
    else:
        url = (
            'https://www.boat24.com/en/secondhandboats/?bre_max=999&bre_min=1&jhr_max=2024&jhr_min=1&lge_max=999&lge_min=1&'
            f'page={20 * i}&rgo%5B0%5D=51&rgo%5B1%5D=31&sort=lgedesc'
    )
    response = requests.get(url)
    with open(ime_datoteke(i), 'w') as dat:
        dat.write(response.text) 

barke = []
for i in range(st_strani):
    with open(ime_datoteke(i)) as dat:
        vsebina = dat.read()
    for blok in vzorec.finditer(vsebina):
        if blok['cena'] != '' and blok['kategorija'] != '':
            barke.append(izloci_podatke_bark(blok.group(0)))

imena_polj = ['id', 'ime', 'kategorija', 'dolzina', 'sirina', 'leto', 'uporabljenost', 'cena', 'lokacija']
with open('barke.csv', 'w', newline='') as dat:
    pisatelj = csv.DictWriter(dat, fieldnames=imena_polj)
    pisatelj.writeheader()
    for barka in barke:
        pisatelj.writerow(barka)

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

kategorije = izloci_gnezdene_podatke(barke)
zapisi_csv(barke, ['id', 'ime', 'dolzina', 'sirina', 'leto', 'uporabljenost', 'cena', 'lokacija'], 'barke_brez_kategorij.csv')
zapisi_csv(kategorije, ['id', 'kategorija'], 'kategorije.csv')

