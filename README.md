# Lyriikan sanojen frekvenssianalyysisovellus *LyrFreq*.

## Aihekuvaus

Sovellus on selainpohjainen tietokantasovellus, jolla voi tarkastella tällä hetkellä suomen-, englannin- ja ranskankielisten kristillisten laululyriikoiden sanafrekvenssejä.

Lyriikkatietokanta on haettu sivustolta [Worship Leader App](https://worshipleaderapp.com/en/download-song-database-opensong-openlp-and-quelea), sisältäen 57 kielen lyriikoita yhteensä 72098 kappaletta. Kyseessä on kristillisten laulujen tietokanta, joiden katsotaan olevan copyright-vapaita lähteitä.

Sovellus hyödyntää *Natural Language Toolkit* -nimistä palvelua ([NLTK](https://www.nltk.org/)), jonka materiaalin avulla voidaan tutkia lingvististä dataa. Sieltä on otettu tähän työhön toiminnot, joilla pilkut, pisteet ym. lisämerkit saa poistettua analysoitavasta datasta. Myös *Stopwordsit* kullekin kielelle on ladattu NLTK:sta. Ne ovat ns. turhia sanoja, kuten suomen *ja, jos, koska, kuin, mutta, niin, sekä, ...*, ja ne poistetaan datasta.

NLTK:n soveltamiseen on otettu mallia sivuston [*Real Python*](https://realpython.com/flask-by-example-part-1-project-setup/) Flask-esimerkkiprojektista.

Sovellukseen on asetettu kuusi oletuslaulua kustakin kolmesta kielestä valmiiksi. Kun sovelluksen käynnistää ensimmäisen kerran ja tietokantataulut syntyvät, tulee laulut syöttää tauluihin. Tämä onnistuu kirjautumalla admin-tunnuksilla sisään, jolloin sivun alalaidassa näkyy kolme nappia: *List users*, *Remove default songs* ja *Add default songs*. Viimeistä nappia painamalla laulut ja niiden tekijät syötetään automaattisesti omiin tauluihinsa sekä liitostiedot liitostauluun. Samoin ne saa tarvittaessa poistettua keskimmäisestä napista.

Löydät sovelluksen osoitteesta [lyrfreq.herokuapp.com](https://lyrfreq.herokuapp.com/).

### Käyttöohje

Kun käyttäjä on kirjautunut sisään avautuu kotinäkymä, jossa näkyvät tilastot laulutietokannasta (kielet, laulut, lauluntekijät) ja sanahakutuloksista (top 5). Näkymään pääsee aina takaisin yläpalkin vasemmassa reunassa olevasta kotinappulasta (*LyrFreq HOME*).

#### Käyttäjäroolit

Sovelluksessa on pysyvä yläpalkki, josta löytyvät sisään- ja uloskirjautumislinkki sekä rekisteröitymislinkki. Valmiita oletuskäyttäjiä ovat *admin* täysillä oikeuksilla (toisten käyttäjien poisto ja roolin vaihdot) sekä *guest* rajoitetuilla (user) oikeuksilla.

Käyttäjä voivat myös luoda oman (user) tilinsä salasanoineen.

Kukin käyttäjä näkee kaikki oletuslaulut sekä itse lisäämänsä laulut. Muiden lisäämiä lauluja ei nähdä. Vain admin voi lisätä yleisesti saatavilla olevia lauluja.

Admin-rooli voi oletuslaulujen lisäämisen ja poistamisen lisäksi tarkastella rekisteröityneitä käyttäjiä sekä poistaa niitä. Admin voi myös asettaa haluamalleen käyttäjälle admin-roolin tai palauttaa sen takaisin peruskäyttäjäksi. Tällä hetkellä oletustunnukset salasanoineen on kovakoodattu helpottamaan asioita esim. katselmuksen suhteen. Loppupalautukseen mennessä kirjautumistiedot poistetaan koodista.

Ohjelmaan voi siis rekisteröityä luomalla omat tunnukset, mutta helpoin tapa kokeilla sovellusta on kirjautua yhtä nappia painamalla vieras-tilille (guest) jolla on peruskäyttäjän oikeudet.

#### Laulut

Yläpalkissa on aluksi estetyt linkit laulujen listaamiseen ja uuden laulun lisäämiseen. Kirjautumisen jälkeen nämä linkit avautuvat toiminnallisiksi.

Laulujen listaus avaa näkymän, jossa laulut ovat listana id:n ja nimen mukaan. Listan yllä on napit listan uudelleenjärjestämiseen aakkosittain nousevasti tai laskeutuvasti sekä ensin kielittäin ja kielen sisällä aakkostetusti.

Kunkin laulun rivin perässä on kolme värillistä nappia, joista sininen näyttää erikseen ko. laulun lyriikan. Näkymästä pääsee takaisin *Back*-nappulasta. Keltainen nappi avaa ko. laulun editointitilaan, jossa voi muokata laulun nimeä, tekijöitä tai lyriikkatekstiä. Näkymässä voi joko palata takaisin tekemättä muutoksia (*Back*) tai asettaa muutos napista *Submit*.

Punaisesta napista laulu poistetaan tietokannasta.

#### Sanafrekvenssit

Sovelluksessa voi tehdä tällä hetkellä pikahakuja yksittäisistä sanoista erikseen kullakin kolmella kielellä.

Yläpalkkiin tulee kirjautumisen jälkeen näkyviin sanan pikahakukenttä kielivalintanappeineen. Tekstilaatikkoon voi kirjoittaa haettavan sanan, minkä jälkeen painetaan halutun kielen nappia, jolla sanasta tehdään kysely tietokantaan. Tällöin näkymä siirtyy tulossivulle. Mikäli sanaa ei löydy, se ilmoitetaan käyttäjälle. Jos sana löytyy, ilmestyy näkymään hakutulos lukumääränä ja pylväskuvaajana.

Näkymään ilmestyy useampi uusi nappi, joiden toiminnot lukevat napeissa. Ylhäällä olevista yhdellä voi suodattaa stopwordsit pois ja toisella tallentaa tuloksen tietokantaan. Alhaalla olevilla napeilla saa avattua sanahaun frekvenssituloksen (top 10) taulukkoina sekä laulujen tekstimassat hakusana merkattuna.

Ohjelma näyttää myös pylväskuvaajan kyseisen kielen laulujen kymmenestä yleisimmästä sanasta. Lisäksi käyttäjä voi nappia painamalla tarkastella kunkin laulun (joista sana löytyi) kohdalla kymmentä yleisintä sanaa taulukkomuodossa tai kyseisiä laulutekstejä, joissa hakusana on merkattu. Tulos esitetään ensin suodattamattomana, eli stopwordsit ovat mukana. Käyttäjä voi tällöin suodattaa tuloksen itse nappia painamalla. Kunkin haun tulokset voi erikseen tallentaa tietokantaan.

#### Pääkäyttäjä (admin)

Pääkäyttäjän kotinäkymässä on vain laulutietokannan sisältö sekä alhaalla kolme nappia, joista voi listata käyttäjät tai lisätä/poistaa laulut.

Käyttäjien listausnäkymässä näkyvät käyttäjien koko nimet, käyttäjänimet sekä rekisteröitymispäivä. Rivien perässä on myös napit käyttäjän poistamiseen ja käyttäjäroolin vaihtamiseen peruskäyttäjästä pääkäyttäjäksi ja päin vastoin.

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
- sanahakuhistorian summia ja keskiarvoja (SUM, AVG) [4 taulua + liitostaulu]
- tietokannan laulu-, lauluntekijä- ja kielitilanne (COUNT) [3 taulua + liitostaulu]

## Tietokannat ja tiedonhaku

### Tietokantataulut

- **User** käyttäjät (taulunimi *account*), sisältäen koko nimen, käyttäjätunnuksen, salasanan, rekisteröintiajan sekä käyttäjäroolin
- **Song** laulut sisältäen laulun nimen, lyriikan, kielen sekä sen käyttäjän id:n, joka on laulun lisännyt
- **Author** laulujen tekijä/tekijät sisältäen nimen
- **Words** sanahakujen tulostaulu (taulunimi *results*) sisältäen hakusanan, löytöjen määrän, tiedot sanafrekvensseistä sekä laulujen id:t
- **Author_song** liitostaulu laulujen ja niiden tekijöiden välillä

## Käyttötapaukset / User stories

Linkissä [*Käyttötapaukset / User stories*](https://github.com/gitjms/Lyriikka-analysaattori/tree/master/documentation/user_stories.md)

## Tietokantakaavio

<img src="https://user-images.githubusercontent.com/46410240/83227690-74c8d180-a18d-11ea-982f-d094c282417c.png" alt="release" width="466" height="578" >

## Myöhemmin tulevia mahdollisia lisäominaisuuksia

* kaikkien 57 maan data mukana
* muitakin kuin vain kristillisiä lyriikoita, eli laulugenret mukaan
* sanafrekvenssit genreittäin
* sanafrekvenssit lauluntekijöiden mukaan
* laulujen tunnetilojen analyysit
* sanan esiintymisfrekvenssien vertailu kielittäin (yhteenvetokyselyt)
* lyhyiden sanayhdistelmien esiintymät ja frekvenssit (yhteenvetokyselyt)
