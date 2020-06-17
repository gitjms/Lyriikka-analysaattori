# Käyttöohje

Sivuston pääsivun yläosa nakyy alla olevassa kuvassa ilman sisäänkirjautumista:

<img src="https://user-images.githubusercontent.com/46410240/84234556-260c2780-aafd-11ea-8182-249cce2f20c6.png" alt="home view" width="500">

Sivun yläosan bannerissa on kaksi linkkiä: *Login* ja *Create account*, joista pääsee kirjautumaan sisään tai rekisteröitymään sovelluksen peruskäyttäjäksi.

Alla olevassa kuvassa näkyy sisäänkirjautumisnäkymä painettaessa *Login*-linkkiä.

<img src="https://user-images.githubusercontent.com/46410240/84234964-c9f5d300-aafd-11ea-9e9f-c64226eb6559.png" alt="login view" width="500">

Alla olevassa kuvassa näkyy rekisteröitymisnäkymä painettaessa *Create account* -linkkiä.

<img src="https://user-images.githubusercontent.com/46410240/84235188-16411300-aafe-11ea-8eb6-f1d2aea6c533.png" alt="register view" width="500">

Kun käyttäjä on kirjautunut sisään pysytään yhä samassa näkymässä eli kotisivulla, mutta sivun yläreunassa näkyy muutoksia:

<img src="https://user-images.githubusercontent.com/46410240/84683879-89081f00-af40-11ea-8f1d-520a364404f1.png" alt="home view logged in" width="500">

Tähän kotinäkymään pääsee mistä tahansa bannerin vasemmassa reunassa olevaa logoa *LyrFreq HOME* klikkaamalla.

Bannerissa on tervehdys kirjautuneelle käyttäjälle, *Logout*-linkki ja sanan pikahakukenttä kielivalintanappeineen. Heti bannerin alapuolella on rivi sivustonappeja, joista pääsee eri sivuille tai tehtyä tiettyjä toimintoja.

Sivustonapeissa olevasta *Stats*-napista pääsee näkymään, jolla näkyvät tilastot laulutietokannasta (kielet, laulut, lauluntekijät) sekä sanahakutuloksista (top 5). Jälkimmäinen ei näy pääkäyttäjälle (admin):

<img src="https://user-images.githubusercontent.com/46410240/84684025-bd7bdb00-af40-11ea-90f4-63a0ab940794.png" alt="stats view" width="500">

Sivustonapeissa olevasta *Info*-napista pääsee näkymään, jossa kerrotaan tarkemmin sivuston tarkoituksesta:

<img src="https://user-images.githubusercontent.com/46410240/84684154-eef4a680-af40-11ea-8af3-66c0d43085a3.png" alt="info view" width="500">

Sivustonappien neljä ensimmäistä nappia ovat pudotusvalikkoja. Ensimmäinen nappi, *Songs*, avaa valikon, jossa ovat linkkipainikkeet *List Songs* ja *Add Song*. Ylempi näistä avaa näkymän, jossa listataan kaikki kyseiselle käyttäjälle luvalliset laulut:

<img src="https://user-images.githubusercontent.com/46410240/84684275-1e0b1800-af41-11ea-869b-925059826b33.png" alt="list songs view" width="500">

Näkymässä voi järjestää lauluja *Sort by* -otsikon alla olevilla napeilla. Kunkin laulurivin perässä on punainen nappi, jolla voi poistaa kyseisen laulun tietokannasta. Sitä painamalla avautuu vahvistusviesti, josta voi vielä peruuttaa toiminnon:

<img src="https://user-images.githubusercontent.com/46410240/84238745-34117680-ab04-11ea-81ad-333a9badbf51.png" alt="list songs view, delete song confirmation" width="500">

Kunkin laulun otsikko on linkki, josta pääsee katsomaan kyseisen laulun lyriikkaa:

<img src="https://user-images.githubusercontent.com/46410240/84684477-60345980-af41-11ea-8cfc-6c29f1001ef0.png" alt="show song view" width="500">

Näkymästä pääsee takaisin listanäkymään *Back*-napista. *Edit*-nappi avaa kyseisen laulun editorissa, jossa otsikkoa, lauluntekijöitä, laulun kielen tai lyriikkaa voi muuttaa:

<img src="https://user-images.githubusercontent.com/46410240/84684592-88bc5380-af41-11ea-8d95-91ebfd19c832.png" alt="edit song view" width="500">

Vierastili ei pääse editointinäkymään. Myös editorissa on *Back*-nappi, josta pääsee takaisin laulunäkymään tekemättä muutoksia.

Pudotusvalikon *Songs* alempi nappi *Add Song* avaa editorin, jossa voi lisätä uuden laulun tietokantaan:

<img src="https://user-images.githubusercontent.com/46410240/84684696-b43f3e00-af41-11ea-9598-fa5af69fa9b3.png" alt="add song view" width="500">

Sivustonappirivin toinen pudotusvalikko *Song Authors* avaa valikon, jossa on linkit *List Song Authors* ja *Top 10 Song Words*. Ylempi näistä avaa näkymän, jolla listataan kaikki tietokannan lauluntekijät:

<img src="https://user-images.githubusercontent.com/46410240/84684843-ecdf1780-af41-11ea-9ee7-3c3c02b838aa.png" alt="list authors view" width="500">

Myös tässä näkymässä kukin lauluntekijä on linkki näkymään, jolla listataan kyseisen henkilön kaikki laulut:

<img src="https://user-images.githubusercontent.com/46410240/84684939-1435e480-af42-11ea-871d-f3bee4d0ca56.png" alt="show author view" width="500">

Ja täällä jälleen kukin laulun otsikko on linkki kyseisen laulun näkymään, samaan johon pääsi laululistan laululinkeistä. Lisäksi tässä näkymässä on nappi *Show Graphs*, joka avaa näkymän kyseisen lauluntekijän kaikkien laulujen sanafrekvensseihin pylväskaaviona ja taulukkoina esitettynä. Näkymässä on myös nappi *Save To Database*, jolla kyseisen lauluntekijän sanafrekvenssit voi tallentaa tietokantaan myöhemmin käsiteltäväksi (ei käytössä vierastilillä).

*Authors*-pudotusvalikon alempi linkki vie näkymään, jossa esitetään koko tietokannan laulujen sanafrekvenssit kielittäin pylväskaavioina sekä kaikkien lauluntekijöiden laulujen sanafrekvenssit taulukkoina. Näkymässä on toiminto turhien sanojen (stopwords) suodattamiseen sekä tulosten tallentamiseen tietokantaan (jälkimmäinen ei käytössä vierastilillä).

Pudotusvalikot *Poems* ja *Poets* toimivat samalla periaattella, kuin *Songs* ja *Song Authors*. Toiminnot ovat samat, mutta laulujen sijaan on runoja ja lauluntekijöiden sijaan runoilijoita.

Bannerin oikealla puolella oleva pikasanahaku vie tulosnäkymään, jossa kyseisen sanan esiintymät lauluissa tai runoissa näytetään pylväskaaviona ja taulukkoina. Myös lyriikat, joista sana löytyy, esitetään hakusana kohostettuna. Tekstilaatikkoon syötetään haettava sana, minkä jälkeen valitaan kieli ja lopuksi valitaan joko laulut tai runot:

<img src="https://user-images.githubusercontent.com/46410240/84685648-4ac02f00-af43-11ea-949c-b5d95456f580.png" alt="word search" width="500">

Alla esimerkki sanan *oh* hakutuloksista englanninkielisistä lauluista:

<img src="https://user-images.githubusercontent.com/46410240/84686531-d1294080-af44-11ea-89e5-39b53694f827.png" alt="word search" width="500">

Kuvan oikeassa yläreunassa ovat napit *Filter Stopwords* (vihreä) ja *Save To Database* (punainen). Ensimmäinen nappi suodattaa tuloksista turhat sanat ja jälkimmäisestä saa tulosdatan tallennettua tietokantaan. Alempana olevat siniset napit *Show/Hide Frequency Table(s)* ja *Show/Hide Song Source(s)* avaavat sanafrekvenssitaulukot ja lyriikoiden tekstimateriaalit. Kuvassa ne on jo aukaistu.

Alla vielä kuva runojen Top 10 frekvenssituloksesta (yläbannerin *Poets*/*Top 10 Poem Words*):

<img src="https://user-images.githubusercontent.com/46410240/84826123-29d30900-b02b-11ea-909f-9e5d34eec9ec.png" alt="top 10 poem words" width="500">

## Käyttäjäroolit

Käyttäjärooleja on kolme: **ADMIN**, **USER** ja **GUEST**. Valmiita oletuskäyttäjiä ovat *admin* täysillä *ADMIN*-oikeuksilla (toisten käyttäjien poisto ja roolin vaihdot sekä oletuslaulujen lisäys ja poisto) sekä *guest* rajoitetuilla **GUEST**-oikeuksilla.

Käyttäjä voivat myös luoda oman (**USER**) tilinsä salasanoineen.

Kukin käyttäjä näkee kaikki oletuslaulut sekä itse lisäämänsä laulut. Muiden lisäämiä lauluja ei nähdä. Vain admin voi lisätä yleisesti saatavilla olevia lauluja, mutta ei myöskään näe käyttäjien itse lisäämiä lauluja.

**ADMIN**-rooli voi oletuslaulujen lisäämisen ja poistamisen lisäksi tarkastella rekisteröityneitä käyttäjiä sekä poistaa niitä. Admin voi myös asettaa haluamalleen käyttäjälle **ADMIN**-roolin tai palauttaa sen takaisin peruskäyttäjäksi eli **USER**-rooliin.

Ohjelmaan voi siis rekisteröityä luomalla omat tunnukset, mutta helpoin tapa kokeilla sovellusta on kirjautua yhtä nappia painamalla vieras-tilille (*guest*) jolla on rajoitetut peruskäyttäjän oikeudet.

Pääkäyttäjällä on joka näkymässä esillä alhaalla viisi nappia, joista voi listata käyttäjät, lisätä oletuslaulut/-runot tietokannasta tai poistaa kaikki laulut/runot.

<img src="https://user-images.githubusercontent.com/46410240/84241534-44c3eb80-ab08-11ea-8f02-25fa71b24a65.png" alt="admin buttons" width="500">

Pääkäyttäjä pääsee käyttäjien listausnäkymään napista *List Users*. Näkymässä näkyvät käyttäjien koko nimet, käyttäjänimet sekä rekisteröitymispäivä. Rivien perässä on lisäksi napit käyttäjän poistamiseen ja käyttäjäroolin vaihtamiseen peruskäyttäjästä pääkäyttäjäksi ja päin vastoin. Kulloinenkin pääkäyttäjä ei voi itse poistaa pääkäyttäjän rooliaan, eikä vierastilin roolia voi muuttaa.

<img src="https://user-images.githubusercontent.com/46410240/83651339-0d15ea80-a5c2-11ea-897c-0ed25e5ea4ab.png" alt="admin dashboard users" width="500">
