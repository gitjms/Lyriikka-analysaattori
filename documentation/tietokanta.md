# Tietokanta

## Tietokantataulut

- **User** käyttäjät (taulunimi *account*), sisältäen koko nimen, käyttäjätunnuksen, salasanan, rekisteröintiajan sekä käyttäjäroolin
  ```
  CREATE TABLE account (
        id INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role INTEGER NOT NULL,
        date_created DATETIME,
        PRIMARY KEY (id),
        UNIQUE (username),
        FOREIGN KEY(role) REFERENCES roles (id)
  );
  ```
- **Role** Taulu käyttäjärooleille
  ```
  CREATE TABLE roles (
        id INTEGER NOT NULL,
        role VARCHAR(255) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (role)
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
        PRIMARY KEY (id),
        FOREIGN KEY(account_id) REFERENCES account (id),
        FOREIGN KEY(account_role) REFERENCES account (role)
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
  CREATE TABLE results (
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
        results_id INTEGER NOT NULL,
        PRIMARY KEY (song_id, results_id),
        FOREIGN KEY(song_id) REFERENCES song (id) ON DELETE cascade,
        FOREIGN KEY(results_id) REFERENCES results (id) ON DELETE cascade
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
        PRIMARY KEY (id),
        FOREIGN KEY(account_id) REFERENCES account (id),
        FOREIGN KEY(account_role) REFERENCES account (role)
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

<img src="https://user-images.githubusercontent.com/46410240/84678924-4e4eb880-af39-11ea-82c5-36b2cb6e9946.png" alt="database diagram">

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
WHERE account.id = ? OR account_role = ?
GROUP BY Song.language
ORDER BY Song.language ASC;
```

missä parametri *account.id* ja *account.role* saavat ulkoiset arvot. Edellinen on kulloisenki käyttäjän oma id ja jälkimmäinen on pääkäyttäjän rooli-id.

---

Seuraavat kaksi kyselyä sijaitsevat *Words*-luokassa (*results*-taulu, *application/words/models.py*). Kyse on jälleen staattisista metodeista *find_words()* ja *find_stats()*. Kyselyiden tulos tulostaa kotisivulle hakusanojen *top 5* -tilanteen (vain peruskäyttäjille). Kyselyt kuuluvat seuraavasti:

```
SELECT DISTINCT results.word,
       COUNT(Song.id) AS w_count,
       SUM(results.matches)
FROM results
JOIN song_result ON song_result.results_id = results.id
JOIN Song ON Song.id = song_result.song_id
JOIN account ON account.id = Song.account_id
WHERE account.id = ? OR account_role = ?
GROUP BY results.word
ORDER BY SUM(results.matches) DESC
LIMIT ?
```

```
SELECT co.matches,
       co.average,
       results.word
FROM results
INNER JOIN (select DISTINCT results.word AS words,
                   SUM(results.matches) AS matches,
                   ROUND( AVG(results.matches), 1 ) AS average
            FROM results
            JOIN song_result ON song_result.results_id = results.id
            JOIN Song ON Song.id = song_result.song_id
            JOIN account ON account.id = Song.account_id
            WHERE account.id = ? OR account_role = ?
            GROUP BY results.word
            ORDER BY matches DESC
) AS co
ON co.words = results.word
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
WHERE (account.id = ? OR account_role = ?) [AND Song.language = ?]
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
WHERE (account.id = ? OR account_role = ?) AND author.id = :id
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
WHERE (account_id = ? OR account_role = ?) [AND Song.language = ?]
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
WHERE (account.id = ? OR account_role = ?) AND Poet.id = :id
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
SELECT results.id AS results_id,
       results.word AS results_word,
       results.matches AS results_matches,
       results.result_all AS results_result_all,
       results.result_no_stop_words AS results_result_no_stop_words
FROM results
WHERE results.result_all = ?
LIMIT ? OFFSET ?
```
missä ensimmäinen parametri saa arvokseen haetun sanan *oh* ja kaksi jälkimmäistä Sqlalchemyn automaattisesti luomat LIMIT ja OFFSET saavat arvoikseen 1 ja 0.
---

Hakutuloksen tallennus tietokantaan tapahtuu seuraavasti:

```
INSERT INTO results (word, matches, result_all, result_no_stop_words)
VALUES (?, ?, ?, ?)
```

Myös liitostauluun tehdään kysely:

```
INSERT INTO song_result (song_id, results_id) VALUES (?, ?)
```

---

Laulujen listaus tapahtuu kyselyllä:

```
SELECT song.id AS song_id,
       song.name AS song_name,
       song.lyrics AS song_lyrics,
       song.language AS song_language,
       song.account_id AS song_account_id
FROM song
WHERE song.account_role = ?
```

---

Listan järjestäminen aakkosten mukaan nousevasti tapahtuu kyselyllä:

```
SELECT song.id AS song_id,
       song.name AS song_name,
       song.lyrics AS song_lyrics,
       song.language AS song_language,
       song.account_id AS song_account_id
FROM song
WHERE song.account_role = ?
ORDER BY song.name ASC
```

Sama laskevassa aakkosjärjestyksessä:

```
SELECT song.id AS song_id,
       song.name AS song_name,
       song.lyrics AS song_lyrics,
       song.language AS song_language,
       song.account_id AS song_account_id
FROM song
WHERE  song.account_role = ?
ORDER BY song.name DESC
```

Järjestäminen kielittäin aakkosjärjestykseen nousevasti:

```
SELECT song.id AS song_id,
       song.name AS song_name,
       song.lyrics AS song_lyrics,
       song.language AS song_language,
       song.account_id AS song_account_id
FROM song
WHERE  song.account_role = ?
ORDER BY song.language, song.name ASC
```

Sama laskevassa aakkosjärjestyksessä:

```
SELECT song.id AS song_id,
       song.name AS song_name,
       song.lyrics AS song_lyrics,
       song.language AS song_language,
       song.account_id AS song_account_id
FROM song
WHERE  song.account_role = ?
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
       song.account_id AS song_account_id
FROM song
WHERE song.id = ?
```

---

Muokatun laulun tallennus tapahtuu seuraavasti:

```
UPDATE song SET name=?, lyrics=? WHERE song.id = ?
```


