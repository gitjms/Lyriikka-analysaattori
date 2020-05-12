# Lyriikan sanojen frekvenssianalyysisovellus *LyrFreq*

## Aihekuvaus

Sovellus on selainpohjainen tietokantasovellus, jolla voi tarkastella suomalaisten kristillisten laululyriikoiden sanafrekvenssejä.
Lyriikkatietokanta on haettu sivustolta [Worship Leader App](https://worshipleaderapp.com/en/download-song-database-opensong-openlp-and-quelea), sisältäen 57 kielen lyriikoita yhteensä 72098 kappaletta. Suomenkielisiä lyriikoita on 358. Kyseessä on kristillisten laulujen tietokanta, joiden katsotaan olevan copyright-vapaita, avoimia lähteitä.

## Toimintoja

- [ ] kirjautuminen, roolit: user ja admin
- [ ] online-käyttäjät näkyvät lukumääränä (paitsi admin)
- [ ] käyttäjien aktiivisuushistoria näkyy (admin)
- [ ] kaikkien sanojen frekvenssit top 10(+)
- [ ] tietyn sanan esiintymät (laululista frekvensseineen)
- [ ] lyhyiden sanayhdistelmien esiintymät ja frekvenssit
- [ ] uusien lyriikoiden lisääminen, vanhojen poistaminen, muokkaus (admin)
- [ ] käyttäjien hallinta (admin)

## User stories

| As ... | I want to ... | so that ... |
| --- | --- |
| *user* | kirjautua sisään | voin tehdä frekvenssianalyysejä |
| *user* | tehdä frekvenssianalyysinä top 10 sanat | näen eniten käytety sanat lauluittain/kielittäin |
| *user* | tehdä frekvenssianalyysin tietyn sanan esiintymistiheydestä | näen missä lauluissa/kielissä esiintymisiä on eniten/vähiten |
| *user* | tehdä frekvenssianalyysinä top 10 lyhyet sanayhdistelmät | näen eniten käytety sanat lauluittain/kielittäin |
| *user* | tehdä frekvenssianalyysin lyhyiden sanayhdistelmien esiintymistiheydestä | näen missä lauluissa/kielissä esiintymisiä on eniten/vähiten |
| *admin* | kirjautua sisään | voin huoltaa lyriikoita tai käyttäjiä |
| *admin* | lisätä lyriikoita | tietokanta saa lisämateriaalia |
| *admin* | poistaa lyriikoita | poisto korjaa jonkin ongelman (esim. copyright) |
| *admin* | muokata lyriikoita | korjaus korjaa virheen lyriikassa |
| *admin* | poistaa käyttäjiä | lopettaneet käyttäjät saadaan pois |

## Tietokantakaavio

Linkissä alustava [tietokantakaavio](https://github.com/gitjms/Lyriikka-analysaattori/blob/master/documentation/db-diagram.png)

## Suunnitellut ominaisuudet

* kaikkien 57 maan data mukana
* lyriikkadatan tarkastelu kielittäin
* tietyn sanan frekvenssi suhteessa kieleen ja koko dataan
* muitakin kuin vain kristillisiä lyriikoita