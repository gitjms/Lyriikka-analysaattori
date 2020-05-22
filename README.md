# Lyriikan sanojen frekvenssianalyysisovellus *LyrFreq*

## Aihekuvaus

Sovellus on selainpohjainen tietokantasovellus, jolla voi tarkastella englanninkielisten kristillisten laululyriikoiden sanafrekvenssejä.

Lyriikkatietokanta on haettu sivustolta [Worship Leader App](https://worshipleaderapp.com/en/download-song-database-opensong-openlp-and-quelea), sisältäen 57 kielen lyriikoita yhteensä 72098 kappaletta. Kyseessä on kristillisten laulujen tietokanta, joiden katsotaan olevan copyright-vapaita lähteitä.

Sovellukseen on asetettu vain kuusi oletuslaulua valmiiksi.

*Stop words* on kopioitu sivulta [Flask by Example](https://realpython.com/flask-by-example-part-1-project-setup/) ja hieman täydennetty. Kyse on turhista sanoista, joita ei haluta laskea mukaan, kuten esimerkiksi lyriikoiden verse- ja chorusosamerkinnät yms.
Parempi olisi käyttää isoja kirjastoja, jotka saa ladattua käyttöön *Natural Language Toolkit* (NLTK) nimisestä palvelusta. Kyseisen alustan datamäärä on kuitenkin niin iso, ettei sitä kannata tässä pikkusovelluksessa käyttää.

Kyseessä on lingvistinen data, jonka avulla voi tehdä monenlaista tiedonlouhintaa kielten parissa. Koko data-arkisto on kooltaan yli 3GT, mutta siitä voi kulloiseenkin tutkimukseen ottaa käyttöön pienemmän osan. Esimerkiksi nettisivujen ja chättien tutkimiseen on oma kirjastonsa, Reuters Corpus pitää puolestaan sisällään yli 1,3 miljoonaa sanaa uutisläteistä, ja Shakespearen tarinoita löytää Gutenberg-korpuksesta.

### Sovellus

Löydät sovelluksen [täältä](https://lyrfreq.herokuapp.com/).

## Suunnitellut toiminnot

### Sivuston toiminta
- [x] kirjautuminen, roolit: user ja admin
- [x] uusien lyriikoiden lisääminen, vanhojen poistaminen, muokkaus
- [x] käyttäjätilien lukumääräinfo (admin)
- [x] käyttäjätilien hallinta (admin)

### Yhteenvetokyselyt
- [ ] kaikkien sanojen frekvenssit top 10(+)
- [ ] tietyn sanan esiintymät (laululista frekvensseineen)
- [ ] lyhyiden sanayhdistelmien esiintymät ja frekvenssit

## Käyttäjät

Valmiita oletuskäyttäjiä ovat *admin* täysillä oikeuksilla (toisten käyttäjien poisto) sekä *guest* rajoitetuilla (user) oikeuksilla.

Käyttäjä voivat myös luoda oman (user) tilinsä salasanoineen.

Kukin käyttäjä näkee kaikki oletuslaulut sekä itse lisäämänsä laulut. Muiden lisäämiä lauluja ei nähdä. Vain admin voi lisätä yleisesti saatavilla olevia lauluja.

## Tietokannat ja tiedonhaku

Tietokantataulut ovt *User* eli käyttäjät, *Song*, eli laulut sekä *Words* eli tulostaulu. Tulostauluun kerätään tiedot sanafrekvensseistä sekä haetun sana esiintymisistä.

## User stories

Linkissä [*User stories*](https://github.com/gitjms/Lyriikka-analysaattori/tree/master/documentation/user_stories.md)

## Tietokantakaavio

Linkissä alustava [tietokantakaavio](https://github.com/gitjms/Lyriikka-analysaattori/blob/master/documentation/images/db-diagram.png)

## Myöhemmin mahdollisia lisäominaisuuksia

* kaikkien 57 maan data mukana
* lyriikkadatan tarkastelu kielittäin
* tietyn sanan frekvenssi suhteessa kieleen ja koko dataan
* muitakin kuin vain kristillisiä lyriikoita