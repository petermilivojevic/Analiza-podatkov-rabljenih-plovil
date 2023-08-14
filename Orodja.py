import os
import csv
import requests
from Preberi_podatke import vzorec, st_html, pot_csv, pot_html, izloci_podatke_bark

def ime_datoteke(st_strani):
    return f"Rabljena-plovila-{st_strani + 1}.html"

def ime_poti(pot_mape, ime_datoteke):
    return os.path.join(pot_mape, ime_datoteke)

def izloci_gnezdene_podatke(barke):
    kategorije = []
    for barka in barke:
        for kategorija in barka.pop('kategorija'):
            kategorije.append({'id': barka['id'], 'kategorija': kategorija})

    kategorije.sort(key=lambda kategorija: (kategorija['id'], kategorija['kategorija']))

    return kategorije

def pripravi_imenik(ime_datoteke):
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def zapisi_html(st_strani=st_html, pot_html_mape=pot_html):
    for i in range(st_strani):
        pripravi_imenik(ime_poti(pot_html_mape, ime_datoteke(i)))
        if i == 0:
            url = (
            'https://www.boat24.com/en/secondhandboats/?src=&cat=&whr=EUR&prs_min=&prs_max=&'
            'lge_min=1&lge_max=999&bre_min=1&bre_max=999&rgo%5B%5D=51&rgo%5B%5D=31&jhr_min=1&'
            'jhr_max=2024&sort=lgedesc'
        )
        else:
            url = (
                'https://www.boat24.com/en/secondhandboats/?bre_max=999&bre_min=1&jhr_max=2024&'
                'jhr_min=1&lge_max=999&lge_min=1&'
                f'page={20 * i}&rgo%5B0%5D=51&rgo%5B1%5D=31&sort=lgedesc'
        )
        response = requests.get(url)
        with open(ime_poti(pot_html_mape, ime_datoteke(i)), 'w') as dat:
            dat.write(response.text) 

def pripravi_podatke(st_strani=st_html, pot_html_mape=pot_html):
    barke = []
    for i in range(st_strani):
        with open(ime_poti(pot_html_mape, ime_datoteke(i))) as dat:
            vsebina = dat.read()
        for blok in vzorec.finditer(vsebina):
            if blok['cena'] and blok['kategorija'] and float(blok['dolzina']) > float(blok['sirina']) and float(blok['dolzina']) < 10 * float(blok['sirina']):
                barke.append(izloci_podatke_bark(blok.group(0)))
    return barke

def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    pripravi_imenik(ime_poti(pot_csv, ime_datoteke))
    with open(ime_poti(pot_csv, ime_datoteke), 'w', encoding='utf-8', newline='') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:    
            writer.writerow(slovar)