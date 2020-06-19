# Asennusohje

## Asennusohje lokaaliin käyttöön (Windows)

Esivaatimukset:

* [Python](https://www.python.org/downloads/), vähintään 3.8 (bcryptin kanssa ongelmia 3.7-versioissa)
* [SQLite](https://www.sqlite.org/download.html)
  - *Precompiled Binaries for Windows*: sqlite-tools-win32-x86-3320200.zip ja sqlite-dll-win64-x86-3320200.zip (64-bit)
* [Git Bash](https://gitforwindows.org/)

Sovellus ladataan GitHub-sivustolta vihreästä napista sivun yläoikealla: [**Clone or download**](https://github.com/gitjms/Lyriikka-analysaattori).

Esimerkiksi lataus zip-tiedostona ja purettuna tuottaa kansion *Lyriikka-analysaattori-master* jonka sisältä löytyvät kaikki tarpeelliset komponentit.
Sanotaan tätä tästedes *työkansioksi*.

Mikäli käytät eri Python-versiota kuin 3.8.3, avaa työkansiossa tiedosto *runtime.txt* jollain tekstieditorilla ja muuta siellä oleva ainoa rivi ```python-3.8.3``` vastaamaan omaa Python-versiotasi.

Pythonin asennuksessa tärkeää on asettaa Winsowsin ympäristömuuttujiin polku Pythonin sijaintiin.

1. Avaa työkansiossa *Git Bash* -terminaali
2. Luo työkansioon Pythonin virtuaaliympäristö *venv* kirjoittamalla terminaaliin komento
   ```
   python -m venv venv
   ```
   HUOM: käytä ensimmäisenä terminä *python3*, mikäli pelkkä *python* ei riitä
3. Aktivoi Pythonin virtuaalinen ympäristö kirjoittamalla terminaaliin komento
   ```
   source venv/Scripts/activate
   ```
   Unix (mac, linux) -käyttäjillä yllä oleva komento olisi:
   ```
   source venv/bin/activate
   ```
   Tähän virtuaaliympäristöön tulevat sovelluksen tarvitsemat riippuvuudet.
4. Asenna riippuvuudet työkansiosta löytyvän tiedoston *requirements.txt* avulla komennolla
   ```
   pip install -r requirements.txt
   ```
5. Käynnistä sovellus komennolla
   ```
   python app.py
   ```
6. Avaa internetselaimessa (esim. Chrome) osoite
   ```
   http://127.0.0.1:5000/
   ```
Nyt sovelluksen pitäisi näkyä selaimen sivulla ja työkansiossa *application*-kansioon on ilmestynyt tyhjä tietokanta *songs.db*.

**TÄRKEÄÄ:**

Ennen kuin voit kirjautua sovellukseen, tulee tietokantaan asettaa oletuskäyttäjät: pääkäyttäjä *admin* ja vierastili *guest* (lokaali käyttö):

7. Avaa Windowsin komentoikkuna tai *PowerShell* (*Git Bash* ei välttämättä toimi tässä).
8. Siirry työkansiossa sijaitsevaan *application*-kansioon ja avaa *SQLite*-yhteys ja *songs*-tietokanta komennoilla
   ```
   sqlite3

   .open songs.db
   ```
9. Luo **ensin** pääkäyttäjä. Pääkayttäjän tunnukset ovat: name='admin', username='admin', password='admin'. Kirjoita komentoikkunaan komento:
   ```
   INSERT INTO account (name, username, password, role_id, date_created) VALUES ('admin', 'admin', 'admin', 1, CURRENT_TIMESTAMP);
   ```
   Tämä on oletus-pääkäyttäjä, joka pääsee kirjautumaan sisään ilman sen kummempia tarkistuksia aikä salasana ole hash-koodattu.
   Jos sovelluksen haluaa räätälöidä itselleen sopivaksi omine pääkäyttäjätunnuksineen ilman Python-koodiin kajoamista, suosittelen seuraavaa proseduuria:
   - Luo uusi peruskäyttäjätunnus, josta haluat pääkäyttäjän, ja kirjaudu ulos
   - Kirjaudu sisään oletus-pääkäyttäjätunnuksilla ja aseta äsken luodun tunnuksen rooli pääkäyttäjäksi, kirjaudu ulos
   - Kirjaudu sisään uusilla tunnuksilla ja poista oletuspääkäyttäjätili
   Nyt on vain yksi pääkäyttäjä, joka on itse luotu ja jonka salasana on hash-koodattu. Sitä ei myöskään näy missään Python-koodissa.
10. Luo seuraavaksi vierastili komennolla
    ```
    INSERT INTO account (name, username, password, role_id, date_created) VALUES ('guest', 'guest', 'guest', 2, CURRENT_TIMESTAMP);
    ```
    Huomaa, että pääkäyttäjän *role*-arvo on aina **1**, kun taas vierastilin vastaava arvo on aina **2**. Muiden peruskäyttäjien rooli on **3**.

    Vierastilin arvo *name* on vapaasti valittavissa. Mikäli halutaan vaihtaa vierastilin tunnukset *username* ja *password*, täytyy muokata tiedostossa *application/auth/views.py* rivejä 87 ja 88:
    ```python
    87	username = "guest"
    88	password = u"guest".encode('utf-8')
    ```
    Ylempään riviin *guest* tilalle tulee kirjoittaa haluttu käyttäjänimi, ja alempaan riviin *guest* tilalle haluttu salasana.
    Tällöin myös *INSERT INTO* -komennon tulee olla muokkauksen mukainen.

    Esimerkki: halutaan vierastili nimellä *vierailija*, käyttäjänimellä *vieras* ja salasanalla *12345*. Muokataan *views.py*-tiedoston rivit:
    ```python
    87	username = "vieras"
    88	password = u"12345".encode('utf-8')
    ```
    Nyt vasta lisätään käyttäjä tietokantaan:
    ```
    INSERT INTO account (name, username, password, role_id, date_created) VALUES ('vierailija', 'vieras', '12345', 2, CURRENT_TIMESTAMP);
    ```
    Vierastilin tulisi olla aina mukana, eli sitä ei saa poistaa.

Nyt sovelluksen pitäisi olla käyttökunnossa ja voit kirjautua sisään äsken luoduilla tunnuksilla tai luoda uuden tunnuksen. Huomaa, että sovelluksen resursseihin on liitetty 18 kappaletta oletuslauluja ja yli 300 runoa, jotka vain pääkäyttäjä voi asentaa tietokantaan.
Mikäli oletuslaulut tai -runot pitää jossain vaiheessa poistaa, on kyse katastrofista, sillä niiden poistaminen poistaa kaikki käyttäjien itse lisäämät laulut ja runot. Eli poistoa tulee käyttää vain hvyin harkiten.

## Asennusohje pilvikäyttöön (Windows)

Jos haluat sovelluksen Herokuun, tarvitset [*Heroku*](https://signup.heroku.com/)-tunnukset ja [*Heroku CLI*](https://devcenter.heroku.com/articles/heroku-cli)n, *Git*-tunnukset (Heroku hallitsee sovellusten käyttöönottoa *Git*illä) sekä *PostgreSQL*n.

Asenna laitteellesi [PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) ja Lisää polku Windowsin ympäristömuuttujiin.

Kirjaudu *Git bash* -terminaalissa työkansiossa Herokuun komennolla:
```
heroku login
```
Terminaaliin ilmestyy teksti, joka pyytää painamaan mitä tahansa näppäintä avatakseen nettisivun Herokun sisäänkirjautumissivulle. Kun olet klikannut nettisivulla sisäänkirjautumisnappia, olet myös *Heroku CLI*:ssä kirjautunut sisään.
Luo sitten sovellukselle paikka Herokussa syöttämällä terminaaliin seuraava komento:
```
heroku create [toivottu-sovelluksen-nimi, eri kuin lyrfreq] --buildpack heroku/python
```
Luo Herokuun tuki ilmaiseen (*hobby-dev*) PostGreSQL-tietokantaan:
```
heroku addons:create heroku-postgresql:hobby-dev
```
Luo Git-repositorio työkansiossa kirjoittamalla *Git bash* -terminaaliin komento
```
git init
```
Kommitoi kaikki Gitiin:
```
git add .

git commit -m "initial commit"
```
Lopuksi puske sovellus Herokuun:
```
git push heroku master
```

**TÄRKEÄÄ:**

Myös Herokussa tulee tietokantaan asettaa oletuskäyttäjät: pääkäyttäjä *admin* ja vierastili *guest*, ennen kuin voit käyttää sovellusta. Toimi seuraavasti:

1. Avaa Windowsin komentoikkuna (*Git Bash* ei välttämättä toimi tässä).
2. Siirry työkansiossa sijaitsevaan *application*-kansioon ja avaa *Heroku-Postgres* -yhteys komennolla
   ```
   heroku pg:psql
   ```
3. Jatka sitten yllä olevista kohdista 9 ja 10.

4. Voit lopuksi sulkea PostGres-yhteyden komennolla ```\q```
5. Avaa sovellus selaimessa syöttämällä terminaaliin komento:
   ```
   heroku open
   ```
   tai kirjoittamalla suoraan nettiosoite:
   ```
   https://[sovelluksen nimi herokussa].herokuapp.com
   ```
   tai avaa sovellus herokun kautta sivuilta löytyvällä napilla *Open app*

---

Mikäli muokkaat sovelluskoodia ja haluat debuggauksen päälle, avaa työkansiossa tiedosto *app.py* jollain teksti- tai koodieditorilla. Tiedostossa on neljä riviä, joista alin on
```python
app.run()
```
Lisää sulkujen sisälle teksti *debug=True*, eli rivi näyttää tällöin seuraavalta:
```python
app.run(debug=True)
```
ja tallenna muutokset.

Sovelluksen ajamisen voi pysäyttää (*Git Bash*) terminaalissa painamalla yhtaikaa ```ctrl+c```.

Kun lopetat työskentelyn, sulje Pythonin virtuaaliympäristö *Git Bashissa* komennolla
```
deactivate
```

Jos muutat tietokantatauluja, siirrä muutokset myös migraatio-repoon työkansiossa syöttämällä *Git Bash* -terminaaliin komennot:
```
flask db migrate -m "[muutoksen aihe]"
```
```
flask db upgrade
```
