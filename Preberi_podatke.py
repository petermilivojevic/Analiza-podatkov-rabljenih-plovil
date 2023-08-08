import re

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