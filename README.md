# Lyriikan sanojen frekvenssianalyysisovellus *LyrFreq*

## Aihekuvaus

Sovellus on selainpohjainen tietokantasovellus, jolla voi tarkastella englanninkielisten kristillisten laululyriikoiden sanafrekvenssejä.

Lyriikkatietokanta on haettu sivustolta [Worship Leader App](https://worshipleaderapp.com/en/download-song-database-opensong-openlp-and-quelea), sisältäen 57 kielen lyriikoita yhteensä 72098 kappaletta. Kyseessä on kristillisten laulujen tietokanta, joiden katsotaan olevan copyright-vapaita lähteitä.

Sovellukseen on asetettu vain viisi oletuslaulua valmiiksi.

Stop-words on kopioitu sivulta [Flask by Example](https://realpython.com/flask-by-example-part-1-project-setup/).

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

Kukin käyttäjä näkee kaikki viisi oletuslaulua sekä itse lisäämänsä laulut. Muiden lisäämiä lauluja ei nähdä. Vain admin voi lisätä yleisesti saatavilla olevia lauluja.


## User stories

Linkissä [*User stories*](https://github.com/gitjms/Lyriikka-analysaattori/tree/master/documentation/user_stories.md)

## Tietokantakaavio

Linkissä alustava [tietokantakaavio](https://github.com/gitjms/Lyriikka-analysaattori/blob/master/documentation/images/db-diagram.png)

## Myöhemmin mahdollisia lisäominaisuuksia

* kaikkien 57 maan data mukana
* lyriikkadatan tarkastelu kielittäin
* tietyn sanan frekvenssi suhteessa kieleen ja koko dataan
* muitakin kuin vain kristillisiä lyriikoita