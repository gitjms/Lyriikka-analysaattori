# Käyttöohje

Sivuston pääsivun yläosa nakyy alla olevassa kuvassa ilman sisäänkirjautumista:

<img src="https://user-images.githubusercontent.com/46410240/84234556-260c2780-aafd-11ea-8182-249cce2f20c6.png" alt="home view">

Sivun yläosan bannerissa on kaksi linkkiä: *Login* ja *Create account*, joista pääsee kirjautumaan sisään tai rekisteröitymään sovelluksen peruskäyttäjäksi.

Alla olevassa kuvassa näkyy sisäänkirjautumisnäkymä painettaessa *Login*-linkkiä.

<img src="https://user-images.githubusercontent.com/46410240/84234964-c9f5d300-aafd-11ea-9e9f-c64226eb6559.png" alt="login view">

Alla olevassa kuvassa näkyy rekisteröitymisnäkymä painettaessa *Create account* -linkkiä.

<img src="https://user-images.githubusercontent.com/46410240/84235188-16411300-aafe-11ea-8eb6-f1d2aea6c533.png" alt="register view">

Kun käyttäjä on kirjautunut sisään pysytään yhä samassa näkymässä eli kotisivulla, mutta sivun yläreunassa näkyy muutoksia:

<img src="https://user-images.githubusercontent.com/46410240/84235329-5accae80-aafe-11ea-8f34-be30981ffddd.png" alt="home view logged in">

Tähän kotinäkymään pääsee mistä tahansa bannerin vasemmassa reunassa olevaa logoa *LyrFreq HOME* klikkaamalla.

Bannerissa on tervehdys kirjautuneelle käyttäjälle, *Logout*-linkki ja sanan pikahakukenttä kielivalintanappeineen. Heti bannerin alapuolella on rivi sivustonappeja, joista pääsee eri sivuille tai tehtyä tiettyjä toimintoja.

Sivustonapeissa olevasta *Stats*-napista pääsee näkymään, jolla näkyvät tilastot laulutietokannasta (kielet, laulut, lauluntekijät) sekä sanahakutuloksista (top 5). Jälkimmäinen ei näy pääkäyttäjälle (admin):

<img src="https://user-images.githubusercontent.com/46410240/84237246-afbdf400-ab01-11ea-94a3-f961f497e934.png" alt="stats view">

Sivustonapeissa olevasta *Info*-napista pääsee näkymään, jossa kerrotaan tarkemmin sivuston tarkoituksesta:

<img src="https://user-images.githubusercontent.com/46410240/84237384-f14e9f00-ab01-11ea-9bcb-b05abbb94760.png" alt="info view">

Sivustonappien kaksi ensimmäistä nappia ovat pudotusvalikkoja. Ensimmäinen nappi, *Songs*, avaa valikon, jossa ovat linkkipainikkeet *List Songs* ja *Add Song*. Ylempi näistä avaa näkymän, jossa listataan kaikki kyseiselle käyttäjälle luvalliset laulut:

<img src="https://user-images.githubusercontent.com/46410240/84237972-fc55ff00-ab02-11ea-885a-6257ea59fac8.png" alt="list songs view">

Näkymässä voi järjestää lauluja *Sort by* -otsikon alla olevilla napeilla. Kunkin laulurivin perässä on punainen nappi, jolla voi poistaa kyseisen laulun tietokannasta. Sitä painamalla avautuu vahvistusviesti, josta voi vielä peruuttaa toiminnon:

<img src="https://user-images.githubusercontent.com/46410240/84238745-34117680-ab04-11ea-81ad-333a9badbf51.png" alt="list songs view, delete song confirmation">

Kunkin laulun otsikko on linkki, josta pääsee katsomaan kyseisen laulun lyriikkaa:

<img src="https://user-images.githubusercontent.com/46410240/84238207-5787f180-ab03-11ea-8a6b-fc052d4eafbc.png" alt="show song view">

Näkymästä pääsee takaisin listanäkymään *Back*-napista. *Edit*-nappi avaa kyseisen laulun editorissa, jossa otsikkoa, lauluntekijöitä, laulun kielen tai lyriikkaa voi muuttaa:

<img src="https://user-images.githubusercontent.com/46410240/84238409-af265d00-ab03-11ea-8775-ebb7959e83f6.png" alt="edit song view">

Vierastili ei pääse editointinäkymään. Myös editorissa on *Back*-nappi, josta pääsee takaisin laulunäkymään tekemättä muutoksia.

Pudotusvalikon *Songs* alempi nappi *Add Song* avaa editorin, jossa voi lisätä uuden laulun tietokantaan:

<img src="https://user-images.githubusercontent.com/46410240/84239110-b1d58200-ab04-11ea-9155-332366011710.png" alt="add song view">

Sivustonappirivin toinen pudotusvalikko *Authors* avaa valikon, jossa on linkit *List Authors* ja *Authors Graph*. Ylempi näistä avaa näkymän, jolla listataan kaikki tietokannan lauluntekijät:

<img src="https://user-images.githubusercontent.com/46410240/84239441-27415280-ab05-11ea-811f-14bc20570722.png" alt="list authors view">

Myös tässä näkymässä kukin lauluntekijä on linkki näkymään, jolla listataan kyseisen henkilön kaikki laulut:

<img src="https://user-images.githubusercontent.com/46410240/84239606-6d96b180-ab05-11ea-9991-65ae573aa1d3.png" alt="show author view">

Ja täällä jälleen kukin laulun otsikko on linkki kyseisen laulun näkymään, samaan johon pääsi laululistan laululinkeistä. Lisäksi tässä näkymässä on nappi *Show Graphs*, joka avaa näkymän kyseisen lauluntekijän kaikkien laulujen sanafrekvensseihin pylväskaaviona ja taulukkoina esitettynä. Näkymässä on myös nappi *Save To Database*, jolla kyseisen lauluntekijän sanafrekvenssit voi tallentaa tietokantaan myöhemmin käsiteltäväksi (ei käytössä vierastilillä).

*Authors*-pudotusvalikon alempi linkki vie näkymään, jossa esitetään koko tietokannan laulujen sanafrekvenssit kielittäin pylväskaavioina sekä kaikkien lauluntekijöiden laulujen sanafrekvenssit taulukkoina. Näkymässä on toiminto turhien sanojen (stopwords) suodattamiseen sekä tulosten tallentamiseen tietokantaan (jälkimmäinen ei käytössä vierastilillä).

Bannerin oikealla puolella oleva pikasanahaku vie tulosnäkymään, jossa kyseisen sanan esiintymät lauluissa näytetään pylväskaaviona ja taulukkoina. Myös lyriikat, joista sana löytyy, esitetään hakusana kohostettuna.

## Käyttäjäroolit

Käyttäjärooleja on kolme: **ADMIN**, **USER** ja **GUEST**. Valmiita oletuskäyttäjiä ovat *admin* täysillä *ADMIN*-oikeuksilla (toisten käyttäjien poisto ja roolin vaihdot sekä oletuslaulujen lisäys ja poisto) sekä *guest* rajoitetuilla **GUEST**-oikeuksilla.

Käyttäjä voivat myös luoda oman (**USER**) tilinsä salasanoineen.

Kukin käyttäjä näkee kaikki oletuslaulut sekä itse lisäämänsä laulut. Muiden lisäämiä lauluja ei nähdä. Vain admin voi lisätä yleisesti saatavilla olevia lauluja, mutta ei myöskään näe käyttäjien itse lisäämiä lauluja.

**ADMIN**-rooli voi oletuslaulujen lisäämisen ja poistamisen lisäksi tarkastella rekisteröityneitä käyttäjiä sekä poistaa niitä. Admin voi myös asettaa haluamalleen käyttäjälle **ADMIN**-roolin tai palauttaa sen takaisin peruskäyttäjäksi eli **USER**-rooliin.

Ohjelmaan voi siis rekisteröityä luomalla omat tunnukset, mutta helpoin tapa kokeilla sovellusta on kirjautua yhtä nappia painamalla vieras-tilille (*guest*) jolla on rajoitetut peruskäyttäjän oikeudet.

Pääkäyttäjällä on joka näkymässä esillä alhaalla kolme nappia, joista voi listata käyttäjät tai lisätä/poistaa laulut tietokannasta.

<img src="https://user-images.githubusercontent.com/46410240/84241534-44c3eb80-ab08-11ea-8f02-25fa71b24a65.png" alt="admin buttons">

Pääkäyttäjä pääsee käyttäjien listausnäkymään napista *List Users*. Näkymässä näkyvät käyttäjien koko nimet, käyttäjänimet sekä rekisteröitymispäivä. Rivien perässä on lisäksi napit käyttäjän poistamiseen ja käyttäjäroolin vaihtamiseen peruskäyttäjästä pääkäyttäjäksi ja päin vastoin. Pääkäyttäjän ja vierastilin rooleja ei voi muuttaa.

<img src="https://user-images.githubusercontent.com/46410240/83651339-0d15ea80-a5c2-11ea-897c-0ed25e5ea4ab.png" alt="admin dashboard users">
