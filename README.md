# Lyriikan sanojen frekvenssianalyysisovellus *LyrFreq*

## Aihekuvaus

Sovellus on selainpohjainen tietokantasovellus, jolla voi tarkastella tällä hetkellä suomen-, englannin- ja ranskankielisten kristillisten laululyriikoiden sanafrekvenssejä.

Lyriikkatietokanta on haettu sivustolta [Worship Leader App](https://worshipleaderapp.com/en/download-song-database-opensong-openlp-and-quelea), sisältäen 57 kielen lyriikoita yhteensä 72098 kappaletta. Kyseessä on kristillisten laulujen tietokanta, joiden katsotaan olevan copyright-vapaita lähteitä.

Sovellus hyödyntää *Natural Language Toolkit* -nimistä palvelua ([NLTK](https://www.nltk.org/)), jonka materiaalin avulla voidaan tutkia lingvististä dataa. Sieltä on otettu tähän työhön toiminnot, joilla pilkut, pisteet ym. lisämerkit saa poistettua analysoitavasta datasta. Myös *Stopwordsit* kullekin kielelle on ladattu NLTK:sta. Ne ovat ns. turhia sanoja, kuten suomen *ja, jos, koska, kuin, mutta, niin, sekä, ...*, ja ne poistetaan datasta.

Sovellukseen on asetettu kuusi oletuslaulua kustakin kolmesta kielestä valmiiksi. Kun sovelluksen käynnistää ensimmäisen kerran ja tietokantataulut syntyvät, tulee laulut syöttää tauluihin. Tämä onnistuu kirjautumalla admin-tunnuksilla sisään, jolloin sivun alalaidassa näkyy kolme nappia: *List users*, ~~*Remove default songs*~~ ja *Add default songs*. Viimeistä nappia painamalla laulut ja niiden tekijät syötetään automaattisesti omiin tauluihinsa sekä liitostiedot liitostauluun. ~~Samoin ne saa tarvittaessa poistettua keskimmäisestä napista.~~

### Sovellus

Sovelluksessa voi tehdä tällä hetkellä pikahakuja yksittäisistä sanoista erikseen kullakin kolmella kielellä. Ohjelma tulostaa etsityn sanan kokonaislukumäärän kyseisen kielen lauluista sekä erikseen lukumäärät kullekin laululle.

Ohjelma näyttää myös pylväskuvaajan kyseisen kielen laulujen kymmenestä yleisimmästä sanasta. Lisäksi käyttäjä voi nappia painamalla tarkastella kunkin laulun (joista sana löytyi) kohdalla kymmentä yleisintä sanaa taulukkomuodossa tai kyseisiä laulutekstejä, joissa hakusana on merkattu. Tulos esitetään ensin suodattamattomana, eli stopwordsit ovat mukana. Käyttäjä voi tällöin suodattaa tuloksen itse nappia painamalla. Kunkin haun tulokset voi erikseen tallentaa tietokantaan.

Admin-rooli voi oletuslaulujen alkuinsertin lisäksi tarkastella rekisteröityneitä käyttäjiä ja poistaa niitä. Admin voi myös asettaa haluamalleen käyttäjälle admin-roolin tai palauttaa sen takaisin peruskäyttäjäksi. Tällä hetkellä oletustunnukset salasanoineen on kovakoodattu, koska on kyse kurssityöstä eikä *oikeasta* ohjelmasta, ja koska se helpottaa asioita esim. katselmuksen suhteen.

Ohjelmaan voi siis rekisteröityä luomalla omat tunnukset, mutta helpoin tapa kokeilla sovellusta on kirjautua yhtä nappia painamalla vieras-tilille (guest) jolla on peruskäyttäjän oikeudet.

Löydät sovelluksen [täältä](https://lyrfreq.herokuapp.com/).

## Suunnitellut toiminnot

### Sivuston toiminta
- [x] kirjautuminen, roolit: user ja admin
- [x] uusien lyriikoiden lisääminen, vanhojen poistaminen, muokkaus ja tarkastelu, sort
- [x] käyttäjätilien poistaminen (admin)
- [x] käyttäjätilien asettaminen admin-rooliin tai peruskäyttäjä-rooliin (admin)
- [x] sanahaku yhdellä sanalla kolmella kielivalinnalla
- [x] sanahaun tulosten tarkastelu taulukkomuodossa, pylväskuvaajana, kohostettuna tekstinä ja lukumääränä

### Yhteenvetokyselyt
- [x] tietyn sanan esiintymät (laululista frekvensseineen) sekä ko. haun laulujen sanojen frekvenssit top 10(+)
- [x] sanahakuhistorian summia ja keskiarvoja (SUM, AVG) [4 taulua + liitostaulu]
- [x] tietokannan laulu-, lauluntekijä- ja kielitilanne (COUNT) [3 taulua + liitostaulu]
- [ ] sanan esiintymisfrekvenssien vertailu kielittäin
- [ ] lyhyiden sanayhdistelmien esiintymät ja frekvenssit

## Käyttäjät

Valmiita oletuskäyttäjiä ovat *admin* täysillä oikeuksilla (toisten käyttäjien poisto ja roolin vaihdot) sekä *guest* rajoitetuilla (user) oikeuksilla.

Käyttäjä voivat myös luoda oman (user) tilinsä salasanoineen.

Kukin käyttäjä näkee kaikki oletuslaulut sekä itse lisäämänsä laulut. Muiden lisäämiä lauluja ei nähdä. Vain admin voi lisätä yleisesti saatavilla olevia lauluja.

## Tietokannat ja tiedonhaku

Tietokantataulut

- **User** käyttäjät (taulunimi *account*), sisältäen koko nimen, käyttäjätunnuksen, salasanan, rekisteröintiajan sekä käyttäjäroolin
- **Song** laulut sisältäen laulun nimen, lyriikan, kielen sekä käyttäjä-id:n joka on laulun lisännyt
- **Author** laulujen tekijä/tekijät sisältäen nimen
- **Words** sanahakujen tulostaulu (taulunimi *results*) sisältäen hakusanan, löytöjen määrän, tiedot sanafrekvensseistä sekä laulujen id:t
- **Author_song** liitostaulu laulujen ja niiden tekijöiden välillä

## User stories

Linkissä [*User stories*](https://github.com/gitjms/Lyriikka-analysaattori/tree/master/documentation/user_stories.md)

## Tietokantakaavio

<img src="https://user-images.githubusercontent.com/46410240/83227690-74c8d180-a18d-11ea-982f-d094c282417c.png" alt="release" width="466" height="578" >

## Myöhemmin mahdollisia lisäominaisuuksia

* kaikkien 57 maan data mukana
* muitakin kuin vain kristillisiä lyriikoita, eli laulugenret mukaan
* sanafrekvenssit genreittäin
* sanafrekvenssit lauluntekijöiden mukaan
* laulujen *tunnetilojen* analyysit
