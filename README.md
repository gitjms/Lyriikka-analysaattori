# Lyriikan sanojen frekvenssianalyysisovellus *LyrFreq*

## Aihekuvaus

Sovellus on selainpohjainen tietokantasovellus, jolla voi tarkastella tällä hetkellä suomen-, englannin- ja ranskankielisten kristillisten laululyriikoiden sanafrekvenssejä.

Lyriikkatietokanta on haettu sivustolta [Worship Leader App](https://worshipleaderapp.com/en/download-song-database-opensong-openlp-and-quelea), sisältäen 57 kielen lyriikoita yhteensä 72098 kappaletta. Kyseessä on kristillisten laulujen tietokanta, joiden katsotaan olevan copyright-vapaita lähteitä.

Sovellus hyödyntää *Natural Language Toolkit* -nimistä palvelua ([NLTK](https://www.nltk.org/)), jonka materiaalin avulla voidaan tutkia lingvististä dataa. Sieltä on otettu tähän työhön toiminnot, joilla pilkut, pisteet ym. lisämerkit saa poistettua analysoitavasta datasta. Myös *Stopwordsit* kullekin kielelle on ladattu NLTK:sta. Ne ovat ns. turhia sanoja, kuten suomen *ja, jos, koska, kuin, mutta, niin, sekä, ...*, ja halutessaan käyttäjä voi poistaa ne tulosdatasta. NLTK:n soveltamiseen on otettu mallia sivuston [*Real Python*](https://realpython.com/flask-by-example-part-1-project-setup/) Flask-esimerkkiprojektista.

Sovellukseen on asetettu kuusi oletuslaulua kustakin kolmesta kielestä valmiiksi. Kun sovelluksen käynnistää ensimmäisen kerran ja tietokantataulut syntyvät, tulee laulut syöttää tauluihin. Tämä onnistuu kirjautumalla admin-tunnuksilla sisään, jolloin sivun alalaidassa näkyy kolme nappia: *List users*, *Remove default songs* ja *Add default songs*. Viimeistä nappia painamalla laulut ja niiden tekijät syötetään automaattisesti omiin tauluihinsa sekä liitostiedot liitostauluun. Samoin ne saa tarvittaessa poistettua keskimmäisestä napista.

Löydät sovelluksen osoitteesta [lyrfreq.herokuapp.com](https://lyrfreq.herokuapp.com/).

## Sovelluksen toiminnot

### Sivuston toiminnot
- kirjautuminen, roolit: user ja admin
- uusien lyriikoiden lisääminen, vanhojen poistaminen, muokkaus ja tarkastelu, sort
- käyttäjätilien poistaminen (admin)
- käyttäjätilien asettaminen admin-rooliin tai peruskäyttäjä-rooliin (admin)
- sanahaku yhdellä sanalla kolmella kielivalinnalla
- sanahaun tulosten tarkastelu taulukkomuodossa, pylväskuvaajana, kohostettuna tekstinä ja lukumääränä

### Yhteenvetokyselyt
- tietyn sanan esiintymät (laululista frekvensseineen) sekä ko. haun laulujen sanojen frekvenssit top 10(+)
- sanahakuhistorian top 5 summia ja keskiarvoja (COUNT, SUM, AVG) [3 taulua + liitostaulu]
- tietokannan laulu-, lauluntekijä- ja kielitilanne (COUNT) [3 taulua + liitostaulu]

## Dokumentteja

[**Käyttöohjeet**](documentation/kayttoohje.md)

[**Asennusohjeet**](documentation/asennusohje.md)

[**Tietokanta**](documentation/tietokanta.md)

[**Käyttäjätarinat ja käyttötapaukset**](documentation/user_stories.md)

## Myöhemmin tulevia mahdollisia lisäominaisuuksia

* kaikkien 57 maan data mukana
* muitakin kuin vain kristillisiä lyriikoita, eli laulugenret mukaan
* sanafrekvenssit genreittäin
* sanafrekvenssit lauluntekijöiden mukaan
* laulujen tunnetilojen analyysit
* sanan esiintymisfrekvenssien vertailu kielittäin (yhteenvetokyselyt)
* lyhyiden sanayhdistelmien esiintymät ja frekvenssit (yhteenvetokyselyt)
* sivutus (pagination)
