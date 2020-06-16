# Lyriikan sanojen frekvenssianalyysisovellus *LyrFreq*

## Aihekuvaus

Sovellus on selainpohjainen tietokantasovellus, jolla voi tarkastella tällä hetkellä suomen-, englannin- ja ranskankielisten runojen sekä kristillisten laululyriikoiden sanafrekvenssejä.

Laululyriikkatietokanta on haettu sivustolta [Worship Leader App](https://worshipleaderapp.com/en/download-song-database-opensong-openlp-and-quelea), sisältäen 57 kielen lyriikoita yhteensä 72098 kappaletta. Kyseessä on kristillisten laulujen tietokanta, joiden katsotaan olevan copyright-vapaita lähteitä.

Sovellus hyödyntää *Natural Language Toolkit* -nimistä palvelua ([NLTK](https://www.nltk.org/)), jonka materiaalin avulla voidaan tutkia lingvististä dataa. Sieltä on otettu tähän työhön toiminnot, joilla pilkut, pisteet ym. lisämerkit saa poistettua analysoitavasta datasta.

*Stopwordsit* kullekin kielelle on noudettu [Count Words Free](https://countwordsfree.com/)-nimiseltä sivustolta ja modifioitu itse. Ne ovat ns. turhia sanoja, kuten suomen *ja, jos, koska, kuin, mutta, niin, sekä, ...*, ja halutessaan käyttäjä voi poistaa ne tulosdatasta. NLTK:n soveltamiseen on otettu mallia sivuston [*Real Python*](https://realpython.com/flask-by-example-part-1-project-setup/) Flask-esimerkkiprojektista.

Sovellukseen on asetettu valmiiksi kuusi oletuslaulua kustakin kolmesta kielestä sekä 374 runoa 1800-luvun runoilijoilta. Kun sovelluksen käynnistää ensimmäisen kerran ja tietokantataulut syntyvät, tulee laulut syöttää tauluihin. Tämä onnistuu kirjautumalla admin-tunnuksilla sisään, jolloin sivun alapalkissa näkyvät napit: *List users*, *Add default songs*, *Remove all songs*, *Add default poems* ja *Remove all poems*. Vihreistä napeista painamalla saa ladattua laulut ja niiden tekijät sekä runot ja runoilijat. Laulut ja runot syötetään automaattisesti omiin tauluihinsa sekä liitostiedot liitostauluihinsa. Samoin ne saa tarvittaessa poistettua punaisista napeista.

Löydät sovelluksen osoitteesta [lyrfreq.herokuapp.com](https://lyrfreq.herokuapp.com/).

## Sovelluksen toiminnot

### Sivuston toiminnot
- kirjautuminen, roolit: peruskäyttäjä *user* ja pääkäyttäjä *admin* sekä vierastili *guest*
- uusien lyriikoiden lisääminen, vanhojen poistaminen, muokkaus ja tarkastelu, sort
- käyttäjätilien poistaminen (admin)
- käyttäjätilien asettaminen admin-rooliin tai peruskäyttäjä-rooliin (admin)
- sanahaku yhdellä sanalla kolmella kielivalinnalla
- sanahaun tulosten tarkastelu taulukkomuodossa, pylväskuvaajana, kohostettuna tekstinä ja lukumääränä

### Yhteenvetokyselyt
- tietyn sanan esiintymät (laululista frekvensseineen) sekä ko. haun laulujen sanojen frekvenssit top 10
- sanahakuhistorian top 5 summia ja keskiarvoja (COUNT, SUM, AVG) [3 taulua + liitostaulu]
- tietokannan laulu-, lauluntekijä- ja kielitilanne (COUNT) [3 taulua + liitostaulu]
- sanafrekvenssit lauluntekijöiden mukaan
- sanafrekvenssit kielittäin

## Dokumentteja

[**Käyttöohjeet**](documentation/kayttoohje.md)

[**Asennusohjeet**](documentation/asennusohje.md)

[**Tietokanta**](documentation/tietokanta.md)

[**Käyttäjätarinat ja käyttötapaukset**](documentation/user_stories.md)

## Myöhemmin tulevia mahdollisia lisäominaisuuksia

* kaikkien 57 maan data mukana
* muita kuin kristillisiä lyriikoita ja laulugenret mukaan
* sanafrekvenssit genreittäin
* laulujen tunnetilojen analyysit
* lyhyiden sanayhdistelmien esiintymät ja frekvenssit (yhteenvetokyselyt)
* yleisimmät (esim top 10) sanat genreittäin ja kielittäin sanapilvinä (word cloud) etusivulla
* dokumenttien kääntäminen englanniksi
* käyttöliittymä monikieliseksi
