# Käyttöohje

Kun käyttäjä on kirjautunut sisään avautuu kotinäkymä, jossa näkyvät tilastot laulutietokannasta (kielet, laulut, lauluntekijät) ja sanahakutuloksista (top 5).

<img src="https://user-images.githubusercontent.com/46410240/83642637-c3c09d80-a5b7-11ea-8ca1-abd3c83971d0.png" alt="home view">

Jälkimmäinen ei näy pääkäyttäjälle. Näkymään pääsee aina takaisin yläpalkin vasemmassa reunassa olevasta kotinappulasta (*LyrFreq HOME*). Yläpalkin oikeassa reunassa on valkoinen kysymysmerkki, jota klikkaamalla aukeaa info-sivu. Infosta löytyy taustaa ja perustelua sana-analyysiprojektille.

Muuten sovelluksen pitäisi olla melko intuitiivinen. Seuraamalla harvojen nappien tekstejä tai otsikoita tietää mitä voi tehdä.

<img src="https://user-images.githubusercontent.com/46410240/83639232-1186d700-a5b3-11ea-904e-2cf30970b7ad.png" alt="banner">

## Käyttäjäroolit

Sovelluksessa on pysyvä yläpalkki, josta löytyvät sisään- ja uloskirjautumislinkki sekä rekisteröitymislinkki. Käyttäjärooleja on kolme: *ADMIN*, *USER* ja *GUEST*. Valmiita oletuskäyttäjiä ovat *admin* täysillä *ADMIN*-oikeuksilla (toisten käyttäjien poisto ja roolin vaihdot) sekä *guest* rajoitetuilla *GUEST*-oikeuksilla.

Käyttäjä voivat myös luoda oman (user) tilinsä salasanoineen.

Kukin käyttäjä näkee kaikki oletuslaulut sekä itse lisäämänsä laulut. Muiden lisäämiä lauluja ei nähdä. Vain admin voi lisätä yleisesti saatavilla olevia lauluja.

Admin-rooli voi oletuslaulujen lisäämisen ja poistamisen lisäksi tarkastella rekisteröityneitä käyttäjiä sekä poistaa niitä. Admin voi myös asettaa haluamalleen käyttäjälle admin-roolin tai palauttaa sen takaisin peruskäyttäjäksi.

Ohjelmaan voi siis rekisteröityä luomalla omat tunnukset, mutta helpoin tapa kokeilla sovellusta on kirjautua yhtä nappia painamalla vieras-tilille (guest) jolla on rajoitetut peruskäyttäjän oikeudet.

<img src="https://user-images.githubusercontent.com/46410240/83640295-9d4d3300-a5b4-11ea-8822-0ec25e4e008a.png" alt="login and create account">

## Laulut

Yläpalkissa on aluksi estetyt linkit laulujen listaamiseen ja uuden laulun lisäämiseen. Kirjautumisen jälkeen nämä linkit avautuvat toiminnallisiksi.

Laulujen listaus avaa näkymän, jossa laulut ovat listana id:n ja nimen mukaan.

<img src="https://user-images.githubusercontent.com/46410240/83645729-7c3c1080-a5bb-11ea-9419-b09ab4a4c712.png" alt="song list">

Listan yllä on napit listan uudelleenjärjestämiseen aakkosittain nousevasti tai laskeutuvasti sekä ensin kielittäin ja kielen sisällä aakkostetusti.

Kunkin laulun rivin perässä on kolme värillistä nappia, joista sininen näyttää erikseen ko. laulun lyriikan. Näkymästä pääsee takaisin *Back*-nappulasta. Keltainen nappi avaa ko. laulun editointitilaan, jossa voi muokata laulun nimeä, tekijöitä tai lyriikkatekstiä. Näkymässä voi joko palata takaisin tekemättä muutoksia (*Back*) tai asettaa muutos napista *Submit*.

Punaisesta napista laulu poistetaan tietokannasta.

<img src="https://user-images.githubusercontent.com/46410240/83646803-d689a100-a5bc-11ea-839f-0db63d1e73e2.png" alt="view and edit song">

## Sanafrekvenssit

Sovelluksessa voi tehdä tällä hetkellä pikahakuja yksittäisistä sanoista erikseen kullakin kolmella kielellä.

Yläpalkkiin tulee kirjautumisen jälkeen näkyviin sanan pikahakukenttä kielivalintanappeineen.

<img src="https://user-images.githubusercontent.com/46410240/83646995-0e90e400-a5bd-11ea-828b-4caca478be5f.png" alt="word search">

Tekstilaatikkoon voi kirjoittaa haettavan sanan, minkä jälkeen painetaan halutun kielen nappia, jolla sanasta tehdään kysely tietokantaan. Tällöin näkymä siirtyy tulossivulle. Mikäli sanaa ei löydy, se ilmoitetaan käyttäjälle. Jos sana löytyy, ilmestyy näkymään hakutulos lukumääränä ja pylväskuvaajana.

<img src="https://user-images.githubusercontent.com/46410240/83647586-bc9c8e00-a5bd-11ea-8e5f-691c56faa01d.png" alt="word search result">

Näkymään ilmestyy useampi uusi nappi, joiden toiminnot lukevat napeissa. Ylhäällä olevista yhdellä voi suodattaa stopwordsit (turhat sanat) pois ja toisella tallentaa tuloksen tietokantaan.

<img src="https://user-images.githubusercontent.com/46410240/83647830-06857400-a5be-11ea-8fe2-4e5ac62d1a61.png" alt="top buttons">

Alhaalla olevilla napeilla saa avattua sanahaun frekvenssituloksen (top 10) taulukkoina sekä laulujen tekstimassat hakusana merkattuna.

<img src="https://user-images.githubusercontent.com/46410240/83647937-25840600-a5be-11ea-8a5c-7cbc57d32a61.png" alt="bottom buttons">

Ohjelma näyttää frekvenssituloksen (top 10) taulukkona erikseen kullekin laululle, josta sana löytyy.

<img src="https://user-images.githubusercontent.com/46410240/83648100-55330e00-a5be-11ea-8aeb-f0f8f84177a2.png" alt="frequency table">

Lisäksi käyttäjä voi nappia painamalla tarkastella kunkin laulun (joista sana löytyi) kohdalla kymmentä yleisintä sanaa taulukkomuodossa tai kyseisiä laulutekstejä, joissa hakusana on merkattu.

<img src="https://user-images.githubusercontent.com/46410240/83648301-8d3a5100-a5be-11ea-81c2-d14dc1b92877.png" alt="match songs">

Tulos esitetään ensin suodattamattomana, eli stopwordsit ovat mukana. Käyttäjä voi tällöin suodattaa tuloksen itse nappia painamalla. Kunkin haun tulokset voi erikseen tallentaa tietokantaan.

## Pääkäyttäjä (admin)

Pääkäyttäjän kotinäkymässä on vain laulutietokannan sisältö sekä alhaalla kolme nappia, joista voi listata käyttäjät tai lisätä/poistaa laulut.

<img src="https://user-images.githubusercontent.com/46410240/83648798-28cbc180-a5bf-11ea-850d-6a5b20f0b5e8.png" alt="admin dashboard">

Käyttäjien listausnäkymässä näkyvät käyttäjien koko nimet, käyttäjänimet sekä rekisteröitymispäivä. Rivien perässä on myös napit käyttäjän poistamiseen ja käyttäjäroolin vaihtamiseen peruskäyttäjästä pääkäyttäjäksi ja päin vastoin. Pääkäyttäjän ja vierastilin rooleja ei voi muuttaa.

<img src="https://user-images.githubusercontent.com/46410240/83651339-0d15ea80-a5c2-11ea-897c-0ed25e5ea4ab.png" alt="admin dashboard users">
