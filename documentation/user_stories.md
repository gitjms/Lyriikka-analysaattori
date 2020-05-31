# Käyttäjätarinat (User stories)

| Roolissa... | haluan... | jotta... | |
| :--- | :--- | :--- | :--- |
| *user* | kirjautua sisään | voin tehdä frekvenssianalyysejä | :heavy_check_mark: |
| *user* | kirjautua sisään | näen tietokannan sisällön | :heavy_check_mark: |
| *user* | tehdä frekvenssianalyysinä <br/> top 10 sanat | näen eniten käytety sanat lauluittain | :heavy_check_mark: |
| *user* | tehdä frekvenssianalyysin <br/> tietyn sanan esiintymistiheydestä | näen missä lauluissa <br/> esiintymisiä on eniten/vähiten | :heavy_check_mark: |

| Roolissa... | haluan... | jotta... | |
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

# Käyttötapauksia (Use cases)

### Käyttötapaus: LyrFreq-sivulle rekisteröityminen

### Käyttötapauksen tyypillinen kulku:
  - Käyttäjä luo tunnuksen antamalla nimensä ja luomalla käyttäjänimen sekä salasanan.

### Sääntöjä:
  - Käyttäjänimen tulee olla uniikki. Ohjelma ilmoittaa mikäli samanlainen käyttäjänimi on jo olemassa ja kehottaa luomaan erilaisen käyttäjänimen.
  - Salasanan tulee olla vähintään 4 merkkiä pitkä.
  - Mikään tekstikenttä ei saa olla tyhjä, eli vähimmäispituus on muissa kuin salasanassa 1 merkki. Ohjelma ilmoittaa mikäli jokin kenttä on tyhjä tai salasana on liian lyhyt.

## Esimerkkejä käyttötapauksen ilmentymästä

### Onnistunut rekisteröityminen

> Sepeteus Sananikkari tulee LyrFreqin pääsivulle, jossa vain kaksi toimintoa on mahdollisia: *Login* ja *Create account*.
  Sepeteus haluaa rekisteröityä sivustolle, joten hän painaa *Create account* -linkkiä.
  Linkki avaa uuden näkymän, jossa on kaksi nappia ja kolme tekstinsyöttökenttää.
  Sepeteus havaitsee ylimmän napin *Cancel* vievän hänet takaisin pääsivulle, joten hän klikka uudestaa *Create account* -linkkiä.
  Seuraavaksi Sepeteus huomaa ylimmässä tekstinsyöttölaatikossa lukevan *Enter Full Name*, ja niinpä hän kirjoittaa laatikkoon *Sepeteus Sananikkari*.
  Tämän jälkeen Sepeteus ohjaa kursorin alempaan tekstinsyöttölaatikkoon, jossa lukee *Enter Username*. Sepeteus keksii nimen: *sanaseppo*, jonka hän kirjoittaa laatikkoon.
  Vielä on jäljellä yksi tekstinsyöttölaatikko *Enter Password*, jonka perässä lukee vielä lisäohjeena *min 4 characters*. Sepeteus päätyy salasanaan *1234*.
  Sepeteus huomaa vielä tekstinsyöttölaatikoden ja vihreän *Create*-napin välissä olevan tekstin ja rastilaatikon: *Remember this session?*.
  Sepeteus ei ole varma, haluaako hän ohjelman muistavan istuntoa, joten hän jättää rastin ruksimatta.
  Sepeteus on vihdoin valmis ja klikkaa vihreää *Create*-nappia, joka vie hänet pääsivulle kirjautuneena.
  Rekisteröitymisen ja kirjautumisen onnistumisesta kertoo yläpalkissa näkyvä teksti: *Hello Sanaseppo* sekä se, että kaksi uutta linkkiä on aktiivisia: *List songs* ja *Add song*.

### Epäonnistunut rekisteröityminen ja sen korjaukset

> Sanelma Sananikkari seuraa Sepeteuksen toimia vierestä ja päättää myös rekisteröityä sivustolle.
  Sanelma toimii samoin kuin Sepeteus, kirjoittaen nimensä *Sanelma Sanaseppo*, käyttäjänimen *sanaseppo* ja salasanan.
  Salasanan hän päättää olevan *4321*, mutta kirjoittaa sen huolimattomasti *432*, eli viimeinen numero jää pois.
  Lopulta Sanelma klikkaa vihreää nappia, mutta sivulle ilmestyy keltainen laatikko muutamaksi sekunniksi, jossa lukee *Create account failed*.
  Sivulle ilmestyi myös teksti: *Fields must not be empty. Check password length.*
  Sanelma tutkii kirjoittamansa tekstit huomaten salasanan olevan yhtä numeroa vajaa ja täydentää sen.
  Klikattuaan vihreää nappia sivulle ilmestyy punainen laatikko muutamaksi sekunniksi, jossa lukee taas *Create account failed*.
  Tällä kertaa sivulle on ilmestynyt erilainen teksti, kuin edelliskerralla: *User already exists. Consider changing username.*
  Sanni vaihtaa käyttäjänimeksi *sanasanna*, jolloin vihreän napin klikkaus ohjaa hänet onnistuneesti pääsivulle rekisteröityneenä ja sisään kirjautuneena.

## Koko sovelluksen käyttötapauskaavio

<img src="https://user-images.githubusercontent.com/46410240/83354534-ff622a00-a361-11ea-9610-ce09d557dd63.png" alt="use case" >

