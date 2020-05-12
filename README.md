# Lyriikan sanojen frekvenssianalyysisovellus *LyrFreq*

## Aihekuvaus

Sovellus on selainpohjainen tietokantasovellus, jolla voi tarkastella suomalaisten kristillisten laululyriikoiden sanafrekvenssejä.
Lyriikkatietokanta on haettu sivustolta [Worship Leader App](https://worshipleaderapp.com/en/download-song-database-opensong-openlp-and-quelea), sisältäen 57 kielen lyriikoita yhteensä 72098 kappaletta. Suomenkielisiä lyriikoita on 358. Kyseessä on kristillisten laulujen tietokanta, joiden katsotaan olevan copyright-vapaita, avoimia lähteitä.

## Toimintoja

* kirjautuminen, roolit: user ja admin
* online-käyttäjät näkyvät lukumääränä (paitsi admin)
* kaikkien sanojen frekvenssit top 10 (ja lisää)
* tietyn sanan esiintymät (laululista frekvensseineen)
* lyhyiden sanayhdistelmien esiintymät ja frekvenssit
* uusien lyriikoiden lisääminen, vanhojen poistaminen, muokkaus (admin)

## Tietokantakaavio

Linkissä alustava [tietokantakaavio](https://github.com/gitjms/Lyriikka-analysaattori/blob/master/documentation/db-diagram.png)

## Suunnitellut ominaisuudet

* kaikkien 57 maan data mukana
* lyriikkadatan tarkastelu kielittäin
* tietyn sanan frekvenssi suhteessa kieleen ja koko dataan
* muitakin kuin vain kristillisiä lyriikoita