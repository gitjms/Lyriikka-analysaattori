# Asennusohje

## Asennusohje lokaaliin käyttöön (Windows)

Esivaatimukset:

* [Python](https://www.python.org/downloads/), vähintään 3.7.3 (mieluiten 3.7.7 Herokun vuoksi)
* [Pip](https://pypi.org/project/pip/)
* [SQLite](https://www.sqlite.org/index.html)
* [Git Bash](https://gitforwindows.org/)

Sovellus ladataan GitHub-sivustolta vihreästä napista sivun yläoikealla: [**Clone or download**](https://github.com/gitjms/Lyriikka-analysaattori).

Esimerkiksi lataus zip-tiedostona ja purettuna tuottaa sisäkkäiset kansiot *Lyriikka-analysaattori-master/Lyriikka-analysaattori-master* joiden sisältä löytyvät kaikki tarpeelliset komponentit. Sanotaan tätä tästedes *työkansioksi*.

1. Avaa työkansiossa *Git Bash* -terminaali
2. Asenna riippuvuudet työkansiosta löytyvän tiedoston *requirements.txt* avulla komennolla
   ```
   pip install -r requirements.txt
   ```
3. Avaa Pythonin virtuaalinen ympäristö kirjoittamalla terminaaliin komento
   ```
   source venv/Scripts/activate
   ```
4. Käynnistä sovellus komennolla
   ````
   python app.py
   ```
5. Avaa internetselaimessa (esim. Chrome) osoite
   ```
   http://127.0.0.1:5000/
   ```
   Nyt sovelluksen pitäisi näkyä selaimen sivulla ja työkansiossa *application*-kansioon on ilmestynyt tyhjä tietokanta *songs.db*.
6. **TÄRKEÄÄ:**
   Ennen kuin voit kirjautua sovellukseen, tulee tietokantaan asettaa oletuskäyttäjät: pääkäyttäjä *admin* ja vierastili *guest*.
   - Avaa Windowsin komentoikkuna (*Git Bash* ei välttämättä toimi *SQLiten* kanssa)
   - Siirry työkansiossa sijaitsevaan *application*-kansioon ja avaa *SQLite-yhteys* komennolla
       ```sqlite3```
   - Avaa tietokanta komennolla
      ```
      .open songs.db
      ```
   - Luo **ensin** pääkäyttäjä. Pääkayttäjän tunnukset (name='admin', username='admin', password='admin') voi vapaasti vaihtaa haluamikseen. Salasanan tulee olla vähintään 4 merkkiä pitkä. Kirjoita komentoikkunaan komento
       ```
       INSERT INTO account (name, username, password, admin, date_created) VALUES ('admin', 'admin', 'admin', True, CURRENT_TIMESTAMP);
   - Luo seuraavaksi vierastili komennolla
       ```
       INSERT INTO account (name, username, password, admin, date_created) VALUES ('guest', 'guest', 'guest', False, CURRENT_TIMESTAMP);
       ```
   - Huomaa, että pääkäyttäjän *admin*-arvo on **True**, kun taas vierastilin arvon on **False**.
   - Vierastilin arvo *name* on vapaasti valittavissa. Mikäli halutaan vaihtaa vierastilin tunnukset *username* ja *password*, täytyy muokata tiedostossa *application/auth/views.py* rivejä 43 ja 44:
     ```python
     43	username = "guest"
     44	password = u"guest".encode('utf-8')
     ```
     - ylempään riviin *guest* tilalle tulee kirjoittaa haluttu käyttäjänimi, ja alempaan riviin *guest* tilalle haluttu salasana.
     - Tällöin myös *INSERT INTO* -koodi tulee olla muokkauksen mukainen.
     - Esimerkki: halutaan vierastili nimellä *vierailija*, käyttäjänimellä *vieras* ja salasanalla *12345*. Muokataan *views.py*-tiedoston rivit:
     ```python
     43	username = "vieras"
     44	password = u"12345".encode('utf-8')
     ```
     ja nyt vasta lisätään käyttäjä tietokantaan:
     ```
     INSERT INTO account (name, username, password, admin, date_created) VALUES ('vierailija', 'vieras', '12345', False, CURRENT_TIMESTAMP);
     ```

Nyt sovelluksen pitäisi olla käyttökunnossa ja voit kirjautua sisään äsken luoduilla tunnuksilla tai luoda uuden tunnuksen. Huomaa, että sovellukseen on liitetty 18 kappaletta oletuslauluja, jotka vain pääkäyttäjä voi asentaa tietokantaan.

Mikäli muokkaat sovelluskoodia ja haluat debuggauksen päälle, avaa työkansiossa tiedosto *app.py* jollain teksti- tai koodieditorilla. Tiedostossa on neljä riviä, joista alin on
```python
app.run()
```
Lisää sulkujen sisälle teksti *debug=True*, eli rivi näyttää tällöin seuraavalta:
```python
app.run(debug=True)
```
ja tallenna muutokset.

Sovelluksen ajamisen voi pysäyttää terminaalissa painamalla yhtaikaa ```ctrl+c```.

Kun lopetat työskentelyn, sulje Pythonin virtuaaliympäristö komennolla
```
deactivate
```
