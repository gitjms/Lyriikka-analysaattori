# User stories

| Roolissa ... | haluan ... | jotta ... | |
| :--- | :--- | :--- | :--- |
| *user* | kirjautua sisään | voin tehdä frekvenssianalyysejä | :heavy_check_mark: |
| *user* | kirjautua sisään | näen tietokannan sisällön | :heavy_check_mark: |
| *user* | tehdä frekvenssianalyysinä <br/> top 10 sanat | näen eniten käytety sanat lauluittain | :heavy_check_mark: |
| *user* | tehdä frekvenssianalyysin <br/> tietyn sanan esiintymistiheydestä | näen missä lauluissa <br/> esiintymisiä on eniten/vähiten | :heavy_check_mark: |

| Roolissa ... | haluan ... | jotta ... | |
| :--- | :--- | :--- | :--- |
| *admin* | kirjautua sisään | voin huoltaa lyriikoita tai käyttäjiä | :heavy_check_mark: |
| *admin* | kirjautua sisään | näen tietokannan sisällön | :heavy_check_mark: |
| *admin* | kirjautua sisään | näen top 5 sanahakuosumat | :heavy_check_mark: |
| *admin* | lisätä lyriikoita | tietokanta saa lisämateriaalia | :heavy_check_mark: |
| *admin* | poistaa lyriikoita | poisto korjaa jonkin <br/> ongelman (esim. copyright) | :heavy_check_mark: |
| *admin* | tyhjentää tietokannan | tyhjentäminen korjaa jonkin vakavan ongelman | :heavy_check_mark: |
| *admin* | muokata lyriikoita | korjaus korjaa virheen laulussa | :heavy_check_mark: |
| *admin* | poistaa käyttäjiä | lopettaneet käyttäjät saadaan pois | :heavy_check_mark: |
| *admin* | muuttaa käyttäjien roolin | peruskäyttäjän voi asettaa väliaikaisesti pääkäyttäjäksi | :heavy_check_mark: |

# Käyttötapaukset

* Käyttötapaus: LyrFreq sivulle kirjautuminen

* Käyttötapauksen tyypillinen kulku:
  - Käyttäjä luo tunnuksen antamalla nimensä ja luomalla käyttäjänimen sekä salasanan.

* Sääntöjä:
  - Käyttäjänimen tulee olla uniikki. Ohjelma ilmoittaa mikäli samanlainen käyttäjänimi on jo olemassa ja kehottaa luomaan erilaisen käyttäjänimen.
  - Salasanan tulee olla vähintään 4 merkkiä pitkä.

## Esimerkki käyttötapauksen ilmentymästä

> Sepeteus Sananikkari tulee LyrFreqin pääsivulle, jossa hän huomaa vain kahden toiminnon olevan mahdollisia: *Login* ja *Create account*.
  Sepeteus haluaa kirjautua sivustolle, joten hän painaa *Create account* -linkkiä.
  Linkki avaa uuden näkymän, jossa on kaksi nappia ja kolme tekstinsyöttökenttää.
  Sepeteus havaitsee ylimmän napin *Cancel* vievän hänet takaisin pääsivulle.
  Seuraavaksi Sepeteus huomaa ylimmässä tekstinsyöttölaatikossa lukevan *Enter Full Name*, ja niinpä hän kirjoittaa laatikkoon *Sepeteus Sananikkari*.
  Tämän jälkeen Sepeteus ohjaa kursorin alempaan tekstinsyöttölaatikkoon, jossa lukee *Enter Username*. Sepeteus keksii nimen: *sanaseppo*, jonka hän kirjoittaa laatikkoon.
  Vielä on jäljellä yksi tekstinsyöttölaatikko *Enter Password*, jonka perässä lukee vielä lisäohjeena *min 4 characters*. Sepeteus päätyy salasanaan *1234*.
  Sepeteus huomaa vielä tekstinsyöttölaatikoden ja vihreän *Create*-napin välissä olevan tekstin ja rastilaatikon: *Remember this session?*.
  Sepeteus ei ole varma, haluaako hän ohjelman muistavan istuntoa, joten hän jättää rastin ruksimatta.
  Sepeteus on vihdoin valmis ja klikkaa tyynesti vihreää *Create*-nappia, joka vie hänet pääsivulle kirjautuneena.
