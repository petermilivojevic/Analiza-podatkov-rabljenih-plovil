from Orodja import izloci_gnezdene_podatke, zapisi_csv, pripravi_podatke, zapisi_html

zapisi_html()

barke = pripravi_podatke()
imena_polj = [
    'id', 'ime', 'kategorija', 'dolzina', 'sirina',
    'leto', 'uporabljenost', 'cena', 'lokacija'
    ]

# Ta csv se ne bo uporabljal v nadalnji analizi, vendar ga bom vseeno obdržal,
# saj mi je bil v veliko pomoč pri preverjanju, če koda deluje pravilno.
zapisi_csv(barke, imena_polj, 'barke.csv')

kategorije = izloci_gnezdene_podatke(barke)
zapisi_csv(barke, imena_polj[:2] + imena_polj[3:], 'barke_brez_kategorij.csv')
zapisi_csv(kategorije, ['id', 'kategorija'], 'kategorije.csv')