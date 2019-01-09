import hashlib
import baza
import sqlite3

conn = sqlite3.connect('filmi.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')


def desetletje_leta(leto):
    return 10 * (leto // 10)


def mozna_desetletja():
    poizvedba = """
        SELECT MIN(leto), MAX(leto)
        FROM film
    """
    min_leto, max_leto = conn.execute(poizvedba).fetchone()
    return list(range(desetletje_leta(min_leto), desetletje_leta(max_leto) + 1, 10))


def stevilo_filmov():
    poizvedba = """
        SELECT COUNT(*)
        FROM film
    """
    (st_filmov,) = conn.execute(poizvedba).fetchone()
    return st_filmov


def stevilo_oseb():
    poizvedba = """
        SELECT COUNT(*)
        FROM oseba
    """
    (st_oseb,) = conn.execute(poizvedba).fetchone()
    return st_oseb


def mozne_vloge():
    """
    Funkcija, ki vrne vse možne vloge.

    >>> mozne_vloge()
    [(1, 'igralec'), (2, 'reziser')]
    """
    poizvedba = """
        SELECT id, naziv
        FROM vloga
        ORDER BY naziv
    """
    return conn.execute(poizvedba).fetchall()


for id, naziv in mozne_vloge():
    if naziv == 'igralec':
        IGRALEC = id
    elif naziv == 'reziser':
        REZISER = id


def poisci_filme(niz):
    """
    Funkcija, ki vrne šifre vseh filmov, katerih naslov vsebuje dani niz.

    >>> poisci_filme('potter')
    [241527, 295297, 304141, 330373, 373889, 417741, 926084, 1201607]
    """
    poizvedba = """
        SELECT id
        FROM film
        WHERE naslov LIKE ?
        ORDER BY leto
    """
    return [id_filma for (id_filma,) in conn.execute(poizvedba, ['%' + niz + '%'])]


def podatki_filmov(idji_filmov):
    """
    Vrne osnovne podatke vseh filmov z danimi IDji.

    >>> podatki_filmov([79470, 71853])
    [(71853, 'Monty Python and the Holy Grail', 1975), (79470, 'Life of Brian', 1979)]
    """
    poizvedba = """
        SELECT id, naslov, leto
        FROM film
        WHERE id IN ({})
    """.format(', '.join(len(idji_filmov) * ['?']))
    return conn.execute(poizvedba, idji_filmov).fetchall()


def podatki_filma(id_filma):
    """
    Vrne podatke o filmu z danim IDjem.

    >>> podatki_filma(71853)
    ('Monty Python and the Holy Grail', 1975, 91, 8.3, ['Comedy', 'Fantasy', 'Adventure'],
     [(92, 'igralec'), (416, 'igralec'), (416, 'reziser'), (1037, 'igralec'), (1385, 'igralec'), (1402, 'reziser')])
    """
    poizvedba = """
        SELECT naslov, leto, dolzina, ocena
        FROM film
        WHERE id = ?
    """
    cur = conn.cursor()
    cur.execute(poizvedba, [id_filma])
    osnovni_podatki = cur.fetchone()
    if osnovni_podatki is None:
        return None
    else:
        naslov, leto, dolzina, ocena = osnovni_podatki
        poizvedba_za_zanre = """
            SELECT zanr.naziv
            FROM zanr
                 JOIN pripada ON zanr.id = pripada.zanr
            WHERE pripada.film = ?
            ORDER BY zanr.naziv
        """
        cur.execute(poizvedba_za_zanre, [id_filma])
        zanri = [vrstica[0] for vrstica in cur.fetchall()]
        poizvedba_za_vloge = """
            SELECT nastopa.oseba, vloga.naziv
            FROM vloga
                 JOIN nastopa ON vloga.id = nastopa.vloga
                 JOIN oseba ON oseba.id = nastopa.oseba
            WHERE nastopa.film = ?
            ORDER BY oseba.ime
        """
        cur.execute(poizvedba_za_vloge, [id_filma])
        vloge = cur.fetchall()
        return naslov, leto, dolzina, ocena, zanri, vloge


def id_zanra(zanr, ustvari_ce_ne_obstaja=False):
    """
    Vrne ID podanega žanra.

    Če žanr še ne obstaja, ga doda v bazo.
    """
    vrstica = conn.execute("SELECT id FROM zanr WHERE naziv = ?", [zanr]).fetchone()
    if vrstica is not None:
        return vrstica[0]
    elif ustvari_ce_ne_obstaja:
        return conn.execute("INSERT INTO zanr (naziv) VALUES (?)", [zanr]).lastrowid
    else:
        return None


def id_osebe(oseba, ustvari_ce_ne_obstaja=False):
    """
    Vrne ID podane osebe.

    Če oseba še ne obstaja, jo doda v bazo.
    """
    vrstica = conn.execute("SELECT id FROM oseba WHERE ime = ?", [oseba]).fetchone()
    if vrstica is not None:
        return vrstica[0]
    elif ustvari_ce_ne_obstaja:
        return conn.execute("INSERT INTO oseba (ime) VALUES (?)", [oseba]).lastrowid
    else:
        return None


def dodaj_film(naslov, dolzina, leto, ocena, metascore,
               glasovi, zasluzek, opis, zanri=[], igralci=[],
               reziserji=[]):
    """
    V bazo doda film ter podatke o njegovih žanrih, igralcih in režiserjih.
    """
    with conn:
        id = conn.execute("""
            INSERT INTO film (naslov, dolzina, leto, ocena,
                            metascore, glasovi, zasluzek, opis)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [naslov, dolzina, leto, ocena,
              metascore, glasovi, zasluzek, opis]).lastrowid
        for zanr in zanri:
            conn.execute("INSERT INTO pripada (film, zanr) VALUES (?, ?)",
                         [id, zanr])
        for igralec in igralci:
            conn.execute("""
                INSERT INTO nastopa (film, oseba, vloga)
                VALUES (?, ?, ?)
            """, (id, igralec, IGRALEC))
        for reziser in reziserji:
            conn.execute("""
                INSERT INTO nastopa (film, oseba, vloga)
                VALUES (?, ?, ?)
            """, (id, reziser, REZISER))
        return id


def poisci_osebe(niz):
    """
    Funkcija, ki vrne IDje vseh oseb, katerih ime vsebuje dani niz.

    >>> poisci_osebe('coen')
    [1053, 1054]
    """
    poizvedba = """
        SELECT id
        FROM oseba
        WHERE ime LIKE ?
        ORDER BY ime
    """
    idji_oseb = []
    for (id_osebe,) in conn.execute(poizvedba, ['%' + niz + '%']):
        idji_oseb.append(id_osebe)
    return idji_oseb


def podatki_oseb(id_oseb):
    """
    Vrne osnovne podatke vseh oseb z danimi IDji.

    >>> podatki_oseb([1053, 1054])
    [(1053, 'Ethan Coen'), (1054, 'Joel Coen')]
    """
    poizvedba = """
        SELECT id, ime
        FROM oseba
        WHERE id IN ({})
    """.format(', '.join('?' for _ in range(len(id_oseb))))
    return conn.execute(poizvedba, id_oseb).fetchall()


def podatki_osebe(id_osebe):
    """
    Vrne podatke o osebi z danim IDjem.

    >>> podatki_osebe(92)
    ('John Cleese', [(71853, 'igralec'), (79470, 'igralec'), (85959, 'igralec'), (95159, 'igralec'), (95159, 'reziser')])
    """
    poizvedba = """
        SELECT ime FROM oseba WHERE id = ?
    """
    cur = conn.cursor()
    cur.execute(poizvedba, [id_osebe])
    osnovni_podatki = cur.fetchone()
    if osnovni_podatki is None:
        return None
    else:
        ime, = osnovni_podatki
        poizvedba_za_vloge = """
            SELECT nastopa.film, vloga.naziv
            FROM vloga
                 JOIN nastopa ON vloga.id = nastopa.vloga
                 JOIN film ON film.id = nastopa.film
            WHERE nastopa.oseba = ?
            ORDER BY film.leto
        """
        vloge = conn.execute(poizvedba_za_vloge, [id_osebe]).fetchall()
        return ime, vloge


def dodaj_vlogo(id_osebe, id_filma, id_vloge):
    poizvedba = """
        INSERT INTO nastopa
        (oseba, film, vloga)
        VALUES (?, ?, ?)
    """
    with conn:
        conn.execute(poizvedba, [id_osebe, id_filma, id_vloge])


def najboljsi_filmi_desetletja(leto):
    desetletje = desetletje_leta(leto)
    poizvedba = """
        SELECT naslov, leto, ocena
        FROM film
        WHERE leto BETWEEN ? AND ?
        ORDER BY ocena DESC
        LIMIT 10
    """
    najboljsi_filmi = conn.execute(poizvedba, [desetletje, desetletje + 9]).fetchall()
    return desetletje, najboljsi_filmi


def seznam_zanrov():
    poizvedba = """
        SELECT id, naziv FROM zanr
        ORDER BY naziv
    """
    return conn.execute(poizvedba).fetchall()


def seznam_oseb():
    poizvedba = """
        SELECT id, ime FROM oseba
        ORDER BY ime
    """
    return conn.execute(poizvedba).fetchall()


def zakodiraj(geslo):
    zakodirano_geslo = hashlib.sha512(geslo.encode()).hexdigest()
    return zakodirano_geslo


def preveri_geslo(uporabnisko_ime, geslo):
    poizvedba = """
        SELECT * FROM uporabniki
        WHERE uporabnisko_ime = ? AND geslo = ?
    """
    uporabnik = conn.execute(
        poizvedba, [uporabnisko_ime, zakodiraj(geslo)]).fetchone()
    return uporabnik is not None


def ustvari_uporabnika(uporabnisko_ime, geslo):
    poizvedba = """
        INSERT INTO uporabniki
        (uporabnisko_ime, geslo)
        VALUES (?, ?)
    """
    with conn:
        conn.execute(poizvedba, [uporabnisko_ime, zakodiraj(geslo)]).fetchone()
        return True
