import re

with open("Poizkusni.html") as dat:
    vsebina = dat.read()

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

for i, ujemanje in enumerate(vzorec.finditer(vsebina), 1):
    print(i, ujemanje.groupdict())

