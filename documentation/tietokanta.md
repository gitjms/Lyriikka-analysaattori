# Tietokanta

## Tietokantataulut

- **User** käyttäjät (taulunimi *account*), sisältäen koko nimen, käyttäjätunnuksen, salasanan, rekisteröintiajan sekä käyttäjäroolin
  ```
  CREATE TABLE account (
        id INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role_id INTEGER NOT NULL,
        date_created DATETIME,
        PRIMARY KEY (id),
        UNIQUE (username),
        FOREIGN KEY(role_id) REFERENCES role (id)
  );
  ```
- **Role** Taulu käyttäjärooleille
  ```
  CREATE TABLE role (
        id INTEGER NOT NULL,
        role VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
  );
  ```
- **Song** laulut sisältäen laulun nimen, lyriikan, kielen sekä sen käyttäjän id:n, joka on laulun lisännyt
  ```
  CREATE TABLE song (
        id INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        lyrics TEXT NOT NULL,
        language VARCHAR(255) NOT NULL,
        account_id INTEGER NOT NULL,
        account_role INTEGER NOT NULL,
        PRIMARY KEY (id)
  );
  ```
- **Author** laulujen tekijä/tekijät sisältäen nimen
  ```
  CREATE TABLE author (
        id INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        result_all JSON,
        result_no_stop_words JSON,
        PRIMARY KEY (id)
  );
  ```
- **Words** sanahakujen tulostaulu (taulunimi *results*) sisältäen hakusanan, löytöjen määrän, tiedot sanafrekvensseistä sekä laulujen id:t
  ```
  CREATE TABLE result (
        id INTEGER NOT NULL,
        word VARCHAR(255) NOT NULL,
        matches INTEGER NOT NULL,
        result_all JSON NOT NULL,
        result_no_stop_words JSON NOT NULL,
        PRIMARY KEY (id)
  );
  ```
- **Author_song** liitostaulu laulujen ja niiden tekijöiden välillä
  ```
  CREATE TABLE author_song (
        author_id INTEGER NOT NULL,
        song_id INTEGER NOT NULL,
        PRIMARY KEY (author_id, song_id),
        FOREIGN KEY(author_id) REFERENCES author (id) ON DELETE cascade,
        FOREIGN KEY(song_id) REFERENCES song (id) ON DELETE cascade
  );
  ```
- **Song_result** liitostaulu laulujen ja sanahakutulosten välillä
  ```
  CREATE TABLE song_result (
        song_id INTEGER NOT NULL,
        result_id INTEGER NOT NULL,
        PRIMARY KEY (song_id, result_id),
        FOREIGN KEY(song_id) REFERENCES song (id) ON DELETE cascade,
        FOREIGN KEY(result_id) REFERENCES result (id) ON DELETE cascade
  );
  ```
- **Poem** runot sisältäen runon nimen, lyriikan, kielen sekä sen käyttäjän id:n, joka on runon lisännyt
  ```
  CREATE TABLE poem (
        id INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        lyrics TEXT NOT NULL,
        language VARCHAR(255) NOT NULL,
        account_id INTEGER NOT NULL,
        account_role INTEGER NOT NULL,
        PRIMARY KEY (id)
  );
  ```
- **Poet** runoilijat sisältäen nimen ja tiedot sanafrekvensseistä
  ```
  CREATE TABLE poet (
        id INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        result_all JSON,
        result_no_stop_words JSON,
        PRIMARY KEY (id)
  );
  ```
- **Poem_poet** liitostaulu runojen ja runoilijoiden välillä
  ```
  CREATE TABLE poet_poem (
        poet_id INTEGER NOT NULL,
        poem_id INTEGER NOT NULL,
        PRIMARY KEY (poet_id, poem_id),
        FOREIGN KEY(poet_id) REFERENCES poet (id) ON DELETE cascade,
        FOREIGN KEY(poem_id) REFERENCES poem (id) ON DELETE cascade
  );
  ```

## Tietokantakaavio

<img src="https://user-images.githubusercontent.com/46410240/85147252-418ed500-b257-11ea-8168-693c1a7a7aef.png" alt="database diagram">

## Tietokantakyselyjä

Sovelluksessa on kiolme automaattista kyselyä, jotka suoritetaan sisäänkirjautuessa. Näiden kyselyjen tulokset tulostetaan kotisivulle, eli ensimmäiselle sivulle sisäänkirjauduttua.

Ensimmäinen kysely on *Song*-luokassa (*application/songs/models.py*) sijaitsevassa staattinen metodi *find_database_songs_status()*. Sen tulos on katsaus tietokannan kulloiseenkin sisältöön. Kysely on seuraavanlainen:

```
SELECT DISTINCT Song.language,
       COUNT(DISTINCT Song.name),
       COUNT(DISTINCT Author.name)
FROM Song
LEFT JOIN author_song ON Song.id = author_song.song_id
LEFT JOIN Author ON author_song.author_id = Author.id
LEFT JOIN account ON account.id = Song.account_id
     AND account.role_id = Song.account_role
WHERE account.id = ? OR account_role = ?
GROUP BY Song.language
ORDER BY Song.language ASC;
```

missä parametri *account.id* ja *account.role* saavat ulkoiset arvot. Edellinen on kulloisenki käyttäjän oma id ja jälkimmäinen on pääkäyttäjän rooli-id.

---

Seuraavat kaksi kyselyä sijaitsevat *Word*-luokassa (*result*-taulu, *application/words/models.py*). Kyse on jälleen staattisista metodeista *find_words()* ja *find_stats()*. Kyselyiden tulos tulostaa kotisivulle hakusanojen *top 5* -tilanteen (vain peruskäyttäjille). Kyselyt kuuluvat seuraavasti:

```
SELECT DISTINCT result.word,
       COUNT(Song.id) AS w_count,
       SUM(result.matches)
FROM result
JOIN song_result ON song_result.result_id = result.id
JOIN Song ON Song.id = song_result.song_id
JOIN account ON account.id = Song.account_id
     AND account.role_id = Song.account_role
WHERE account.id = ? OR account_role = ?
GROUP BY result.word
ORDER BY SUM(result.matches) DESC
LIMIT ?
```

```
SELECT co.matches,
       co.average,
       result.word
FROM result
INNER JOIN (select DISTINCT result.word AS words,
                   SUM(result.matches) AS matches,
                   ROUND( AVG(result.matches), 1 ) AS average
            FROM result
            JOIN song_result ON song_result.result_id = result.id
            JOIN Song ON Song.id = song_result.song_id
            JOIN account ON account.id = Song.account_id
                 AND account.role_id = Song.account_role
            WHERE account.id = ? OR account_role = ?
            GROUP BY result.word
            ORDER BY matches DESC
) AS co
ON co.words = result.word
GROUP BY co.matches, co.words, results.word, co.average
ORDER BY co.matches DESC
LIMIT ?
```

Parametrien kaksi ensimmäistä arvoa tulevat tässä samalla periaatteella kuin edellisissä kyselyesimerkeissäkin, mutta kolmas arvo termille *LIMIT* on 5.

---

Näiden lisäksi on muita staattisia metodeja, joita kutsutaan myöhemmin koodista. Näistä kaksi sijaitsee *Author*-luokassa (*application/authors/models.py*). Kyseessä ovat metodit *get_authors()* ja *get_authorsongs()*. Edellinen tuottaa listan lauluntekijöistä lauluineen, joka esitetään *Authors*-sivulla. Kysely on seuraavanlainen:

```
SELECT DISTINCT author.name,
       STRING_AGG (Song.name,'; ') songs,
       Song.language,
       author.id
FROM Song
INNER JOIN author_song ON author_song.song_id = Song.id
INNER JOIN author ON author.id = author_song.author_id
JOIN account ON account.id = Song.account_id
     AND account.role_id = Song.account_role
WHERE account.id = ? OR account_role = ? [AND Song.language = ?]
GROUP BY author.name, Song.language, author.id
ORDER BY Song.language, author.name ASC;
```

Käyttäjäparametrien arvot tulevat jälleen samalla periaatteella kuin edellisissä kyselyesimerkeissä. Toisella rivillä oleva *STRING_AGG* toimii vain PostGres-kyselyssä Herokussa. SQLite-kyselyssä tulee käyttää termiä *GROUP_CONCAT*. *WHERE* lauseen perässä hakasuluissa oleva osa on tyhjä, mikäli metodia kutsutaan tiedoston *authors/views.py* metodista *authors_list()*, jolla tulostetaan kaikki lauluntekijät. Jos sen sijaan kutsu tulee saman tiedoston metodista *authors_graph()*, jolla tulostetaan kaikkien laulujen sanafrekvenssit kielittäin, tulee hakasulkuosioon sen sisällä oleva lause ja kieleksi haluttu arvo.
Jälkimmäinen kysely (*get_authorsongs()*) tuottaa listan tietyn lauluntekijän laluista. Kysely on seuraavanlainen:

```
SELECT Song.id,
       Song.lyrics,
       Song.name,
       Song.language
FROM Song
LEFT JOIN author_song ON Song.id = author_song.song_id
LEFT JOIN Author ON author_song.author_id = Author.id
LEFT JOIN account ON account.id = Song.account_id
     AND account.role_id = Song.account_role
WHERE account.id = ? OR account_role = ? AND author.id = :id
GROUP BY Song.id, Song.lyrics, Song.name, Song.language;
```

Parametreinä jälleen käyttäjän id, pääkäyttäjän rooli-id sekä halutun lauluntekijän id.

Myös *Poet*-luokassa (*application/poets/models.py*) on staattisia metodeja. Kyseessä ovat metodit *get_poets()* ja *get_poetpoems()*. Edellinen tuottaa listan runoilijoista runoineen, joka esitetään *Poets*-sivulla. Kysely on seuraavanlainen:

```
SELECT DISTINCT poet.name,
       STRING_AGG (Poem.name,'; ') poems,
       Poem.language,
       Poet.id
FROM Poet
INNER JOIN poet_poem ON poet_poem.poet_id = Poet.id
INNER JOIN Poem ON Poem.id = poet_poem.poem_id
JOIN account ON account.id = Poem.account_id
     AND account.role_id = Poem.account_role
WHERE account_id = ? OR account_role = ? [AND Song.language = ?]
GROUP BY Poet.name, Poem.language, Poet.id
ORDER BY Poem.language, Poet.name ASC;
```

Käyttäjäparametrien arvot tulevat jälleen samalla periaatteella kuin edellisissä kyselyesimerkeissä. Toisella rivillä oleva *STRING_AGG* toimii vain PostGres-kyselyssä Herokussa. SQLite-kyselyssä tulee käyttää termiä *GROUP_CONCAT*. *WHERE* lauseen perässä hakasuluissa oleva osa on tyhjä, mikäli metodia kutsutaan tiedoston *poets/views.py* metodista *poets_list()*, jolla tulostetaan kaikki runoilijat. Jos sen sijaan kutsu tulee saman tiedoston metodista *poets_graph()*, jolla tulostetaan kaikkien runojen sanafrekvenssit kielittäin, tulee hakasulkuosioon sen sisällä oleva lause ja kieleksi haluttu arvo.
Jälkimmäinen kysely (*get_poetpoems()*) tuottaa listan tietyn runoilijan runoista. Kysely on seuraavanlainen:

```
SELECT Poem.id,
       Poem.lyrics,
       Poem.name,
       Poem.language
FROM Poem
LEFT JOIN poet_poem ON Poem.id = poet_poem.poem_id
LEFT JOIN Poet ON poet_poem.poet_id = Poet.id
LEFT JOIN account ON account.id = Poem.account_id
     AND account.role_id = Poem.account_role
WHERE account.id = ? OR account_role = ? AND Poet.id = :id
GROUP BY Poem.id, Poem.lyrics, Poem.name, Poem.language;
```

Parametreinä jälleen käyttäjän id, pääkäyttäjän rooli-id sekä halutun runoilijan id.

---

Sanahaun Sqlalchemy-kysely esimerkiksi englanninkielisellä termillä *oh* tehdään seuraavan kyselyn avulla:

```
SELECT song.id AS song_id,
       song.lyrics AS song_lyrics,
       song.name AS song_name,
       song.language AS song_language
FROM song
WHERE song.account_role = ? AND song.language = ?
```

Ensimmäinen syötetty parametrin arvo on käyttäjän id ja toinen arvo on tässä esimerkissä ```'english'```, viitaten haetun sanan kielivalintaan.
Kielihakutuloksesta rajataan vielä haettu sana:
```
SELECT result.id AS result_id,
       result.word AS result_word,
       result.matches AS result_matches,
       result.result_all AS result_result_all,
       result.result_no_stop_words AS result_result_no_stop_words
FROM result
WHERE result.result_all = ?
LIMIT ? OFFSET ?
```
missä ensimmäinen parametri saa arvokseen haetun sanan *oh* ja kaksi jälkimmäistä Sqlalchemyn automaattisesti luomat LIMIT ja OFFSET saavat arvoikseen 1 ja 0.
---

Hakutuloksen tallennus tietokantaan tapahtuu seuraavasti:

```
INSERT INTO result (word, matches, result_all, result_no_stop_words)
VALUES (?, ?, ?, ?)
```

Myös liitostauluun tehdään kysely:

```
INSERT INTO song_result (song_id, result_id) VALUES (?, ?)
```

---

Laulujen listaus tapahtuu kyselyllä:

```
SELECT song.id AS song_id,
       song.name AS song_name,
       song.lyrics AS song_lyrics,
       song.language AS song_language,
       song.account_id AS song_account_id,
       song.account_role AS song_account_role
FROM song
WHERE song.account_id = ? OR song.account_role = ?
```

---

Listan järjestäminen aakkosten mukaan nousevasti tapahtuu kyselyllä:

```
SELECT song.id AS song_id,
       song.name AS song_name,
       song.lyrics AS song_lyrics,
       song.language AS song_language,
       song.account_id AS song_account_id,
       song.account_role AS song_account_role
FROM song
WHERE song.account_id = ? OR song.account_role = ?
ORDER BY song.name ASC
```

Sama laskevassa aakkosjärjestyksessä:

```
SELECT song.id AS song_id,
       song.name AS song_name,
       song.lyrics AS song_lyrics,
       song.language AS song_language,
       song.account_id AS song_account_id,
       song.account_role AS song_account_role
FROM song
WHERE song.account_id = ? OR song.account_role = ?
ORDER BY song.name DESC
```

Järjestäminen kielittäin aakkosjärjestykseen nousevasti:

```
SELECT song.id AS song_id,
       song.name AS song_name,
       song.lyrics AS song_lyrics,
       song.language AS song_language,
       song.account_id AS song_account_id,
       song.account_role AS song_account_role
FROM song
WHERE song.account_id = ? OR song.account_role = ?
ORDER BY song.language, song.name ASC
```

Sama laskevassa aakkosjärjestyksessä:

```
SELECT song.id AS song_id,
       song.name AS song_name,
       song.lyrics AS song_lyrics,
       song.language AS song_language,
       song.account_id AS song_account_id,
       song.account_role AS song_account_role
FROM song
WHERE song.account_id = ? OR song.account_role = ?
ORDER BY song.language, song.name DESC
```

---

Uuden laulun lisääminen tietokantaan tapahtuu kyselyllä:

```
INSERT INTO song (name, lyrics, language, account_id)
VALUES (?, ?, ?, ?)
```

---

Laulun avaaminen lukutilaan:

```
SELECT song.id AS song_id,
       song.name AS song_name,
       song.lyrics AS song_lyrics,
       song.language AS song_language,
       song.account_id AS song_account_id,
       song.account_role AS song_account_role
FROM song
WHERE song.id = ?
```

---

Muokatun laulun tallennus tapahtuu seuraavasti:

```
UPDATE song SET name=?, lyrics=? WHERE song.id = ?
```


