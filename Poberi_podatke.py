import requests
from Preberi_podatke import vzorec, izloci_podatke_bark
from Orodja import ime_datoteke, izloci_gnezdene_podatke, zapisi_csv
import csv

st_strani = 59
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

kategorije = izloci_gnezdene_podatke(barke)
zapisi_csv(barke, ['id', 'ime', 'dolzina', 'sirina', 'leto', 'uporabljenost', 'cena', 'lokacija'], 'barke_brez_kategorij.csv')
zapisi_csv(kategorije, ['id', 'kategorija'], 'kategorije.csv')