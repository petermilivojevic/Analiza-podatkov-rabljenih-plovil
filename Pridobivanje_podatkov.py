import re
import requests
import csv

vzorec = re.compile(
    r'<p class="blurb__title-header">(?P<kategorija>[^<]*)</p>'
    r'<h3 class="blurb__title">[^>]*>(?P<ime>[^<]*)</a></h3>'
    r'<p class="blurb__subtitle">[^<]*</p>'
    r'<ul class="blurb__facts"><li class="blurb__fact"><span class="blurb__value">(?P<dimenzija>[^<]*)</span>.*\n'
    r'<li class="blurb__fact">(.*|.*\n.*)(?!<li class="blurb__fact l-hide--lg-u">)li class="blurb__fact l-hide--lg-u">'
    r'<span class="blurb__value">(?P<leto>[^<]*)</span>'
    r'.*<p class="blurb__location">(?P<lokacija>[^<]*)'
    r'.*<p class="blurb__price">[^\d]*(?P<cena>[\d\.]*)[^<]*'
    r'.*<ul class="blurb__description"><li>(?P<uporabljenost>[^<]*)'
)

def izloci_podatke_bark(blok):
    barka = vzorec.search(blok).groupdict()
    barka['ime'] = barka['ime']
    barka['kategorija']  = barka['kategorija'].strip().split(', ')
    barka['dimenzija'] = barka['dimenzija']
    barka['leto'] = int(barka['leto'])
    barka['uporabljenost'] = barka['uporabljenost']
    barka['cena'] = barka['cena'].replace('.', '')
    barka['lokacija'] = barka['lokacija']
    return barka





def ime_datoteke(st_strani):
    return f"Rabljena-plovila-{st_strani + 1}.html"

for i in range(58):
    if i == 1:
        url = (
        'https://www.boat24.com/en/secondhandboats/?bre_max=999&bre_min=1&lge_max=999&lge_min=1&rgo%5B0%5D=51&rgo%5B1%5D=31'
    )
    else:
        url = (
            'https://www.boat24.com/en/secondhandboats/?bre_max=999&bre_min=1&lge_max=999&lge_min=1&'
            f'page={20 * i}&rgo%5B0%5D=51&rgo%5B1%5D=31'
    )
    response = requests.get(url)
    with open(ime_datoteke(i), 'w') as dat:
        dat.write(response.text) 

barke = []

for i in range(58):
    with open(ime_datoteke(i)) as dat:
        vsebina = dat.read()
    for blok in vzorec.finditer(vsebina):
        barke.append(izloci_podatke_bark(blok.group(0)))

with open('barke.csv', 'w', newline='') as dat:
    pisatelj = csv.writer(dat)
    for barka in barke:
        ime, kategorija, dimenzija, leto = barka['ime'], barka['kategorija'], barka['dimenzija'], barka['leto']
        uporabljenost, cena, lokacija = barka['uporabljenost'], barka['cena'], barka['lokacija']
        pisatelj.writerow([ime, kategorija, dimenzija, leto, uporabljenost, cena, lokacija])


#for i, ujemanje in enumerate(vzorec.finditer(vsebina), 1):
#    print(i, ujemanje.groupdict())
