# käyttäjätarinat ja Käyttötapaukset
User stories, Use cases

## Käyttäjätarinat (User stories)

| Roolissa... | haluan... | jotta... | |
| :--- | :--- | :--- | :--- |
| *user* | kirjautua sisään | voin tehdä frekvenssianalyysejä | :heavy_check_mark: |
| *user* | kirjautua sisään | näen tietokannan sisällön | :heavy_check_mark: |
| *user* | tehdä frekvenssianalyysinä <br/> top 10 sanat | näen eniten käytety sanat lyyrikoittain/kielittäin | :heavy_check_mark: |
| *user* | tehdä frekvenssianalyysin <br/> tietyn sanan esiintymistiheydestä | näen missä lyriikassa <br/> esiintymisiä on eniten/vähiten | :heavy_check_mark: |

| Roolissa... | haluan... | jotta... | |
| :--- | :--- | :--- | :--- |
| *admin* | kirjautua sisään | voin huoltaa lyriikoita tai käyttäjiä | :heavy_check_mark: |
| *admin* | kirjautua sisään | näen tietokannan sisällön | :heavy_check_mark: |
| *admin* | lisätä lyriikoita | tietokanta saa lisämateriaalia | :heavy_check_mark: |
| *admin* | poistaa lyriikoita | poisto korjaa jonkin <br/> ongelman (esim. copyright) | :heavy_check_mark: |
| *admin* | tyhjentää tietokannan | tyhjentäminen korjaa jonkin vakavan ongelman | :heavy_check_mark: |
| *admin* | muokata lyriikoita | korjaus korjaa virheen lyriikassa | :heavy_check_mark: |
| *admin* | poistaa käyttäjiä | lopettaneet käyttäjät saadaan pois | :heavy_check_mark: |
| *admin* | muuttaa käyttäjien roolin | peruskäyttäjän voi asettaa väliaikaisesti pääkäyttäjäksi | :heavy_check_mark: |

## Käyttötapaukset (Use cases)

Esimerkki käyttötapauksen ilmentymästä

* Käyttötapaus: LyrFreq-sivulle rekisteröityminen

* Käyttötapauksen tyypillinen kulku:
  - Käyttäjä luo tunnuksen antamalla nimensä ja luomalla käyttäjänimen sekä salasanan.
  - Salasana syötetään kahteen kertaan varmistukseksi.

* Sääntöjä:
  - Käyttäjänimen tulee olla uniikki ja pituuden enintään 25 merkkiä. Ohjelma ilmoittaa mikäli samanlainen käyttäjänimi on jo olemassa ja kehottaa luomaan erilaisen käyttäjänimen.
  - Salasanan tulee olla vähintään 4 ja enintään 10 merkkiä pitkä.
  - Mikään tekstikenttä ei saa olla tyhjä, eli vähimmäispituus on muissa kuin salasanassa 1 merkki. Ohjelma ilmoittaa mikäli jokin kenttä on tyhjä tai salasana on liian lyhyt.
  - Molempien salasanasyöttöjen tulee olla samanlaiset.

---

Tekstiesimerkkejä käyttötapauksesta *rekisteröityminen*

### Onnistunut rekisteröityminen

> Sepeteus Sananikkari tulee LyrFreqin pääsivulle, jossa vain kaksi toimintoa on mahdollisia: *Login* ja *Create account*.
  Sepeteus haluaa rekisteröityä sivustolle, joten hän painaa *Create account* -linkkiä.
  Linkki avaa uuden näkymän, jossa on kaksi nappia ja kolme tekstinsyöttökenttää.
  Sepeteus havaitsee ylimmän napin *Cancel* vievän hänet takaisin pääsivulle, joten hän klikka uudestaa *Create account* -linkkiä.
  Seuraavaksi Sepeteus huomaa ylimmän tekstinsyöttölaatikon otsikossa lukevan *Full Name*, ja niinpä hän kirjoittaa laatikkoon *Sepeteus Sananikkari*.
  Tämän jälkeen Sepeteus ohjaa kursorin alempaan tekstinsyöttölaatikkoon, jonka otsikossa lukee *Username* ja laatikossa *max 25 characters*. Sepeteus keksii nimen: *sanaseppo*, jonka hän kirjoittaa laatikkoon.
  Vielä on jäljellä kaksi tekstinsyöttölaatikkoa: *Password* ja *Repeat Password*. Ensimmäisessä näistä lukee lisäohjeena *min 4, max 10 characters*. Sepeteus päätyy salasanaan *1234*.
  Sepeteus huomaa vielä tekstinsyöttölaatikoden ja vihreän *Create*-napin välissä olevan tekstin ja rastilaatikon: *Remember this session?*.
  Sepeteus ei ole varma, haluaako hän ohjelman muistavan istuntoa, joten hän jättää rastin ruksimatta.
  Sepeteus on vihdoin valmis ja klikkaa *Register*-nappia, joka vie hänet pääsivulle kirjautuneena.
  Rekisteröitymisen ja kirjautumisen onnistumisesta kertoo yläpalkissa näkyvä teksti: *Hello Sanaseppo* sekä se, että sivun yläbanneriin on ilmestynyt tekstinsyöttölaatikko kolmen napin kera ja bannerin alapuolelle rivi muita nappeja: *Songs*, *Authors*, *Stats* ja *Info*.

### Epäonnistunut rekisteröityminen ja sen korjaukset

> Sanelma Sananikkari seuraa Sepeteuksen toimia vierestä ja päättää myös rekisteröityä sivustolle.
  Sanelma toimii samoin kuin Sepeteus, kirjoittaen nimensä *Sanelma Sanaseppo*, käyttäjänimen *sanaseppo* ja salasanan.
  Salasanan hän päättää olevan *4321*, mutta kirjoittaa sen huolimattomasti *432*, eli viimeinen numero jää pois.
  Lopulta Sanelma klikkaa *Register*-nappia, mutta salasanalaatikon alle ilmestyy teksti, jossa lukee *Field must be between 4 and 10 characters long*.
  Sanelma kirjoittaa salasanan uudestaan, ja klikattuaan vihreää nappia sivulle ilmestyy punainen laatikko muutamaksi sekunniksi, jossa lukee taas *Create account failed*.
  Tällä kertaa sivulle on ilmestynyt erilainen teksti, kuin edelliskerralla: *User already exists. Consider changing username.*
  Sanni vaihtaa käyttäjänimeksi *sanasanna*, jolloin *Register*-napin klikkaus ohjaa hänet onnistuneesti pääsivulle rekisteröityneenä ja sisään kirjautuneena.

## Sovelluksen käyttötapauskaavio

<img src="https://user-images.githubusercontent.com/46410240/84679098-83f3a180-af39-11ea-91ce-077025d41808.png" alt="use case" >

Värikoodien merkitys:
- vihreä on kaikille käyttäjärooleille sallittu
- sininen on vain pääkäyttäjälle sallittu
- punainen on sallittu kirjautuneelle peruskäyttäjälle sekä pääkäyttäjälle

Kuva ei ole kovin selkeä, joten alla vielä kuvat erikseen kunkin käyttäjäroolin osalta:

### Käyttötapauskaaviot erikseen kullekin roolille

<img src="https://user-images.githubusercontent.com/46410240/84679127-9077fa00-af39-11ea-8f29-19e063a01482.png" alt="use case admin" >

<img src="https://user-images.githubusercontent.com/46410240/84679158-9cfc5280-af39-11ea-9753-115d91b91b74.png" alt="use case guest" >

<img src="https://user-images.githubusercontent.com/46410240/84679187-a71e5100-af39-11ea-974a-c8b4cd1c2b26.png" alt="use case user" >