# Käyttöohje

Kun käyttäjä on kirjautunut sisään avautuu kotinäkymä, jossa näkyvät tilastot laulutietokannasta (kielet, laulut, lauluntekijät) ja sanahakutuloksista (top 5). Jälkimmäinen ei näy pääkäyttäjälle. Näkymään pääsee aina takaisin yläpalkin vasemmassa reunassa olevasta kotinappulasta (*LyrFreq HOME*).

## Käyttäjäroolit

Sovelluksessa on pysyvä yläpalkki, josta löytyvät sisään- ja uloskirjautumislinkki sekä rekisteröitymislinkki. Valmiita oletuskäyttäjiä ovat *admin* täysillä oikeuksilla (toisten käyttäjien poisto ja roolin vaihdot) sekä *guest* rajoitetuilla (user) oikeuksilla.

Käyttäjä voivat myös luoda oman (user) tilinsä salasanoineen.

Kukin käyttäjä näkee kaikki oletuslaulut sekä itse lisäämänsä laulut. Muiden lisäämiä lauluja ei nähdä. Vain admin voi lisätä yleisesti saatavilla olevia lauluja.

Admin-rooli voi oletuslaulujen lisäämisen ja poistamisen lisäksi tarkastella rekisteröityneitä käyttäjiä sekä poistaa niitä. Admin voi myös asettaa haluamalleen käyttäjälle admin-roolin tai palauttaa sen takaisin peruskäyttäjäksi. Tällä hetkellä oletustunnukset salasanoineen on kovakoodattu helpottamaan asioita esim. katselmuksen suhteen. Loppupalautukseen mennessä kirjautumistiedot poistetaan koodista.

Ohjelmaan voi siis rekisteröityä luomalla omat tunnukset, mutta helpoin tapa kokeilla sovellusta on kirjautua yhtä nappia painamalla vieras-tilille (guest) jolla on peruskäyttäjän oikeudet.

## Laulut

Yläpalkissa on aluksi estetyt linkit laulujen listaamiseen ja uuden laulun lisäämiseen. Kirjautumisen jälkeen nämä linkit avautuvat toiminnallisiksi.

Laulujen listaus avaa näkymän, jossa laulut ovat listana id:n ja nimen mukaan. Listan yllä on napit listan uudelleenjärjestämiseen aakkosittain nousevasti tai laskeutuvasti sekä ensin kielittäin ja kielen sisällä aakkostetusti.

Kunkin laulun rivin perässä on kolme värillistä nappia, joista sininen näyttää erikseen ko. laulun lyriikan. Näkymästä pääsee takaisin *Back*-nappulasta. Keltainen nappi avaa ko. laulun editointitilaan, jossa voi muokata laulun nimeä, tekijöitä tai lyriikkatekstiä. Näkymässä voi joko palata takaisin tekemättä muutoksia (*Back*) tai asettaa muutos napista *Submit*.

Punaisesta napista laulu poistetaan tietokannasta.

## Sanafrekvenssit

Sovelluksessa voi tehdä tällä hetkellä pikahakuja yksittäisistä sanoista erikseen kullakin kolmella kielellä.

Yläpalkkiin tulee kirjautumisen jälkeen näkyviin sanan pikahakukenttä kielivalintanappeineen. Tekstilaatikkoon voi kirjoittaa haettavan sanan, minkä jälkeen painetaan halutun kielen nappia, jolla sanasta tehdään kysely tietokantaan. Tällöin näkymä siirtyy tulossivulle. Mikäli sanaa ei löydy, se ilmoitetaan käyttäjälle. Jos sana löytyy, ilmestyy näkymään hakutulos lukumääränä ja pylväskuvaajana.

Näkymään ilmestyy useampi uusi nappi, joiden toiminnot lukevat napeissa. Ylhäällä olevista yhdellä voi suodattaa stopwordsit pois ja toisella tallentaa tuloksen tietokantaan. Alhaalla olevilla napeilla saa avattua sanahaun frekvenssituloksen (top 10) taulukkoina sekä laulujen tekstimassat hakusana merkattuna.

Ohjelma näyttää myös pylväskuvaajan kyseisen kielen laulujen kymmenestä yleisimmästä sanasta. Lisäksi käyttäjä voi nappia painamalla tarkastella kunkin laulun (joista sana löytyi) kohdalla kymmentä yleisintä sanaa taulukkomuodossa tai kyseisiä laulutekstejä, joissa hakusana on merkattu. Tulos esitetään ensin suodattamattomana, eli stopwordsit ovat mukana. Käyttäjä voi tällöin suodattaa tuloksen itse nappia painamalla. Kunkin haun tulokset voi erikseen tallentaa tietokantaan.

## Pääkäyttäjä (admin)

Pääkäyttäjän kotinäkymässä on vain laulutietokannan sisältö sekä alhaalla kolme nappia, joista voi listata käyttäjät tai lisätä/poistaa laulut.

Käyttäjien listausnäkymässä näkyvät käyttäjien koko nimet, käyttäjänimet sekä rekisteröitymispäivä. Rivien perässä on myös napit käyttäjän poistamiseen ja käyttäjäroolin vaihtamiseen peruskäyttäjästä pääkäyttäjäksi ja päin vastoin.
