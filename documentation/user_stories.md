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
  Nopeasti Sepeteus havaitsee ylimmän napin *Cancel* vievän hänet takaisin pääsivulle.
  Seuraavaksi tarkkasilmäinen Sepeteus huomaa ylimmässä tekstinsyöttölaatikossa lukevan *Enter Full Name*, ja niinpä hän kirjoittaa laatikkoon *Sepeteus Sananikkari*.
  Tämän jälkeen Sepeteus luontevasti ohjaa kursorin alempaan tekstinsyöttölaatikkoon, jossa lukee *Enter Username*. Kekseliäänä tunnettu Sepeteus loihtii nopeasti leikillisen, mutta häntä osuvasti kuvailevan nimen: *sanaseppo*, jonka hän kirjoittaa laatikkoon.
  Vielä on jäljellä yksi tekstinsyöttölaatikko *Enter Password*, jonka perässä lukee vielä lisäohjeena *min 4 characters*. Tovin pohdittuaan Sepeteus päätyi nokkelaan salasanaan *1235*. Nokkelaan siksi, etteivät numerot juokse aivan tasaisessa, normaalisti opitussa, järjestyksesssä, vaan hyppää yhden numeron yli.
  Mielissään kaikesta tähän astisesta, Sepeteus on viemässä hiiren kursoria kohti hämmästyttävän värikylläistä vihreää nappia *Create*, jonka aprikoi viimein toteuttavan toiveensa tulla sivuston viralliseksi käyttäjäksi. Kuinka ollakaan, Sepeteus huomaa viime tipassa tekstinsyöttölaatikoden ja vihreän napin välissä olevan tekstin ja rastilaatikon: *Remember this session?*.
  Sepeteus ei ole varma, haluaako hän ohjelman muistavan istuntoa, joten hän jättää rastin ruksimatta.
  Sepeteus on vihdoin valmis ja klikkaa tyynesti vihreänä hohtavaa nappia, joka vie hänet ... yhä samalle pääsivulle.
  Sepeteus toipuu kuitenkin nopeasti lievästä pettymyksestä huomatessaan kahden tähän asti estetyn linkin olevan valmiita klikattavaksi: *List songs* ja *Add song*.
  Hän klikkaa jännittyneenä ensimmäistä linkkiä, joka avaa hänen silmiinsä uskomattoman näyn: pitkä listä laulunnimiä, värikkäitä nappeja, suodattimia...
  Sepeteus kokeilee kaikkea - suodattaa laulurivejä aakkosittain ja kielittäin joka suuntaan, tarkastelee joitakin hienoja lyriikoita, editoi pari biisiä tunnistamattomaksi ja jopa puolivahingossa deletoi puolet kappaleista.
  Hän on päässyt laulujen maailmaan, jossa voi tehdä mitä vain!
  Viimein Sepeteus kokeilee yläpalkissa näkyvää tekstinsyöttölaatikkoa *Quick Word Search* kirjoittamalla siihen sanan *oh*. Sepeteus ei voi uskoa silmiään, sillä näkymä vaihtui salamannopeasti toiseksi, jossa on värikästä ongrafiikkaa ja paljon lisää nappeja.
  Kyseessä on sanahaun tulossivu, pohtii Sepeteus mielessään tutkien tulosta.