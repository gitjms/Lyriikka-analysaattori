# Lyriikan sanojen frekvenssianalyysisovellus *LyrFreq*

## Aihekuvaus

Sovellus on selainpohjainen tietokantasovellus, jolla voi tarkastella tällä hetkellä suomen-, englannin- ja ranskankielisten kristillisten laululyriikoiden sanafrekvenssejä.

Lyriikkatietokanta on haettu sivustolta [Worship Leader App](https://worshipleaderapp.com/en/download-song-database-opensong-openlp-and-quelea), sisältäen 57 kielen lyriikoita yhteensä 72098 kappaletta. Kyseessä on kristillisten laulujen tietokanta, joiden katsotaan olevan copyright-vapaita lähteitä.

Sovellukseen on asetettu kuusi oletuslaulua kustakin kolmesta kielestä valmiiksi. Kun sovelluksen käynnistää ensimmäisen kerran ja tietokantataulut syntyvät, tulee laulut syöttää tauluihin. Tämä onnistuu kirjautumalla admin-tunnuksilla sisään, jolloin sivun alalaidassa näkyy kaksi nappia: *List users* ja *Add default songs*. Jälkimmäistä nappia painamalla laulut ja niiden tekijät syötetään automaattisesti omiin tauluihinsa sekä liitostiedot liitostauluun.

*Stop words*, eli turhien sanojen lista, on haettu *Natural Language Toolkit* (NLTK) nimisestä palvelusta. Kyseessä on lingvistinen data, jonka avulla voi tehdä monenlaista tiedonlouhintaa kielten parissa. Koko data-arkisto on kooltaan yli 3GT, mutta siitä voi kulloiseenkin tutkimukseen ottaa käyttöön pienemmän osan. Esimerkiksi nettisivujen ja chättien tutkimiseen on oma kirjastonsa, Reuters Corpus pitää puolestaan sisällään yli 1,3 miljoonaa sanaa uutisläteistä, ja Shakespearen tarinoita löytää Gutenberg-korpuksesta.

### Sovellus

Löydät sovelluksen [täältä](https://lyrfreq.herokuapp.com/).

Sovelluksessa voi tehdä tällä hetkellä pikahakuja yksittäisistä sanoista erikseen kullakin kolmella kielellä. Ohjelma tulostaa etsityn sanan kokonaislukumäärän kyseisen kielen lauluista sekä erikseen lukumäärät kullekin laululle.

Ohjelma näyttää myös pylväskuvaajan kyseisen kielen laulujen kymmenestä yleisimmästä sanasta. Lisäksi käyttäjä voi nappia painamalla tarkastella kunkin laulun (joista sana löytyi) kohdalla kymmentä yleisintä sanaa taulukkomuodossa tai kyseisiä laulutekstejä, joissa hakusana on merkattu.

Admin-rooli voi oletuslaulujen alkuinsertin lisäksi tarkastella rekisteröityneitä käyttäjiä ja poistaa niitä. Admin voi myös asettaa haluamalleen käyttäjälle admin-roolin tai palauttaa sen takaisin peruskäyttäjäksi.

Ohjelmaan voi siis rekisteröityä luomalla omat tunnukset, mutta helpoin tapa kokeilla sovellusta on kirjautua yhdellä napilla vieras-tilille (guest) jolla on peruskäyttäjän oikeudet.

## Suunnitellut toiminnot

### Sivuston toiminta
- [x] kirjautuminen, roolit: user ja admin
- [x] uusien lyriikoiden lisääminen, vanhojen poistaminen, muokkaus ja tarkastelu
- [x] käyttäjätilien poistaminen (admin)
- [x] käyttäjätilien asettaminen admin-rooliin tai peruskäyttäjä-rooliin (admin)
- [x] sanahaku yhdellä sanalla kolmella kielivalinnalla
- [x] sanahaun tulosten tarkastelu taulukkomuodossa, pylväskuvaajana, kohostettuna tekstinä ja lukumääränä

### Yhteenvetokyselyt
- [x] kaikkien sanojen frekvenssit top 10(+)
- [x] tietyn sanan esiintymät (laululista frekvensseineen)
- [ ] lyhyiden sanayhdistelmien esiintymät ja frekvenssit

## Käyttäjät

Valmiita oletuskäyttäjiä ovat *admin* täysillä oikeuksilla (toisten käyttäjien poisto) sekä *guest* rajoitetuilla (user) oikeuksilla.

Käyttäjä voivat myös luoda oman (user) tilinsä salasanoineen.

Kukin käyttäjä näkee kaikki oletuslaulut sekä itse lisäämänsä laulut. Muiden lisäämiä lauluja ei nähdä. Vain admin voi lisätä yleisesti saatavilla olevia lauluja.

## Tietokannat ja tiedonhaku

Tietokantataulut

- **User** eli käyttäjät (taulunimi *account*), sisältäen koko nimen, käyttäjätunnuksen, salasanan, rekisteröintiajan sekä käyttäjäroolin
- **Song**, eli laulut sisältäen laulun nimen, lyriikan, kielen sekä käyttäjä-id:n joka on laulun lisännyt
- **Author** eli laulujen tekijä/tekijät sisältäen nimen
- **Words** eli sanahakujen tulostaulu (taulunimi *results*) sisältäen hakusanan, löytöjen määrän, tiedot sanafrekvensseistä sekä laulujen id:t
- **Author_song** eli liitostaulu laulujen ja niiden tekijöiden välillä

## User stories

Linkissä [*User stories*](https://github.com/gitjms/Lyriikka-analysaattori/tree/master/documentation/user_stories.md)

## Tietokantakaavio

Linkissä alustava [tietokantakaavio](https://github.com/gitjms/Lyriikka-analysaattori/blob/master/documentation/images/db-diagram.png)

## Myöhemmin mahdollisia lisäominaisuuksia

* kaikkien 57 maan data mukana
* lyriikkadatan tarkastelu kielittäin
* tietyn sanan frekvenssi suhteessa kieleen ja koko dataan
* muitakin kuin vain kristillisiä lyriikoita