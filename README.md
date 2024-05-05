# Keskustelusovellus

Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

## Sovelluksen ominaisuuksia:

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun aloitusviestin sisällön.
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- Käyttäjä voi poistaa luomansa ketjun tai viestin
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- Käyttäjä voi poistaa oman käyttäjänsä ja vaihtaa salasanan
- Käyttäjän voi tällä hetkellä lisätä ylläpitäjäksi vain käyttämällä tietokantaa


### Esimerkki käynnistysohjeista

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

```
DATABASE_URL="postgresql:/USERNAME:PASSWORD@localhost/chat"

SECRET_KEY=""
``` 

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla
```
$ python3 -m venv venv

$ source venv/bin/activate

$ pip install -r ./requirements.txt
```

Määritä tietokannan skeema komennolla

```
$ psql < databases.sql
```
Nyt voit käynnistää sovelluksen komennolla

```
$ flask run
```

Jotta voit lisätä uusia keskustelualueita, tee luomastasi käyttäjästä ylläpitäjä seuraavalla komennolla:

```
INSERT INTO admin (user_id, admin_status) VALUES ([user_id], 1);
```

