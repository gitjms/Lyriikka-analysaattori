# Lyriikan sanojen frekvenssianalyysisovellus *LyrFreq*

## Aihekuvaus

Sovellus on selainpohjainen tietokantasovellus, jolla voi tarkastella suomalaisten kristillisten laululyriikoiden sanafrekvenssejä.

Lyriikkatietokanta on haettu sivustolta [Worship Leader App](https://worshipleaderapp.com/en/download-song-database-opensong-openlp-and-quelea), sisältäen 57 kielen lyriikoita yhteensä 72098 kappaletta. Suomenkielisiä lyriikoita on 358. Kyseessä on kristillisten laulujen tietokanta, joiden katsotaan olevan copyright-vapaita lähteitä.

### Sovellus

Löydät sovelluksen [täältä](https://lyrfreq.herokuapp.com/).

## Suunnitellut toiminnot

- [x] kirjautuminen, roolit: guest, admin ja uudet tilit
- [ ] online-käyttäjät näkyvät lukumääränä (paitsi admin)
- [ ] käyttäjien aktiivisuushistoria näkyy (admin)
- [ ] kaikkien sanojen frekvenssit top 10(+)
- [ ] tietyn sanan esiintymät (laululista frekvensseineen)
- [ ] lyhyiden sanayhdistelmien esiintymät ja frekvenssit
- [ ] uusien lyriikoiden lisääminen, vanhojen poistaminen, muokkaus (admin)
- [ ] käyttäjien hallinta (admin)

## Käyttäjäroolit

Käyttäjätili *admin* on pääkäyttäjä, joka voi poistaa muita käyttäjiä.

Muut käyttäjätilit ovat tasaveroisia oikeuksiltaan.

Tili *guest* on vierailijatili, jonka kirjautumistiedot on kovakoodattu sovellukseen.

Kukin sovelluksen käyttäjä voi halutessaan luoda oman tilin nimellään, käyttäjänimellä ja salasanalla.

Guest-tili on helpoin tapa kokeilla sovellusta (sandbox).

## User stories

Linkissä [*User stories*](https://github.com/gitjms/Lyriikka-analysaattori/tree/master/documentation/user_stories.md)

## Tietokantakaavio

Linkissä alustava [tietokantakaavio](https://github.com/gitjms/Lyriikka-analysaattori/blob/master/documentation/images/db-diagram.png)

## Myöhemmin mahdollisia lisäominaisuuksia

* kaikkien 57 maan data mukana
* lyriikkadatan tarkastelu kielittäin
* tietyn sanan frekvenssi suhteessa kieleen ja koko dataan
* muitakin kuin vain kristillisiä lyriikoita
  * lyriikkadatan tarkastelu kielittäin/genreittäin
  * tietyn sanan frekvenssi suhteessa kieleen/genreen ja koko dataan