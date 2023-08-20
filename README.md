# Analiza-podatkov-rabljenih-plovil
Analiziral sem nekaj več kot 1000 ponudb rabljenih plovil, ki se prodajajo v Sloveniji in na Hrvaškem na spletni strani [Boat24](https://www.boat24.com/en/). Analiza je predstavljena v datoteki [Analiza.ipynb](Analiza.ipynb).

Za vsako plovilo sem zajel podatke:
* id, ki se uporablja na spletni strani
* ime plovila v oglasu
* dolžino plovila
* širino plovila
* leto izdelave
* podatek ali je barka rabljena ali ne
* ceno
* lokacijo oziroma državo v kateri se prodaja
* kategorije ki jim barka pripada

Postavljene hipoteze:
1. V povprečju so najdraže barke, ki spadajo v kategorijo superjaht (Superyacht)
2. Na Hrvaškem so boljše ponudbe za nakup barke kot v Sloveniji
3. Razpon cen plovil na kvadratni meter je večji kot pri stanovanjih
4. Na prodaj so plovila s primerno kvadraturo za bivanje, ki so cenovno ugodnejše za nakup kot stanovanja
5. Večina bark, ki ne spadajo v kategorije katamaran in trimaran (Catamaran, Power Catamaran in Trimaran) ima razmerje med širino in dolžino med 1:5 in 1:5 + 2,5m dolžine

## Priprava podatkov
Podatke sem zajel iz spletne strani [Boat24](https://www.boat24.com/en/) in jih zapisal v html obliki v mapi [Barke_html](Barke_html) in csv obliki v mapi [Barke_csv](Barke_csv) s skripto [Poberi_podatke.py](Poberi_podatke.py), ki pa za pravilno delovanje potrebuje še skripti [Preberi_podatke.py](Preberi_podatke.py) in [Orodja.py](Orodja.py).

Zapisani csv-ji so:
* [barke.csv](barke.csv), ki ima zapisane vse zajete podatke in je služil zgolj preverjanju pravilnosti delovanja programa
* [barke_brez_kategorij.csv](barke_brez_kategorij.csv), ki vsebuje vse podatke razen kategorij
* [kategorije.csv](kategorije.csv), ki vsebuje le id-je bark in kaegorije
Takšna razdelitev csv-jev je bila potrebna za lažjo nadalnjo analizo zaradi dejstva, da spadajo nekatere barke v več kategorij.