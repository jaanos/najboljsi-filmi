import baza
import sqlite3

conn = sqlite3.connect('filmi.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')


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
    osnovni_podatki = conn.execute(poizvedba, [id_filma]).fetchone()
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
        zanri = [vrstica[0] for vrstica in conn.execute(
            poizvedba_za_zanre, [id_filma]).fetchall()]
        poizvedba_za_vloge = """
            SELECT nastopa.oseba, vloga.naziv
            FROM vloga
                 JOIN nastopa ON vloga.id = nastopa.vloga
                 JOIN oseba ON oseba.id = nastopa.oseba
            WHERE nastopa.film = ?
            ORDER BY oseba.ime
        """
        vloge = conn.execute(poizvedba_za_vloge, [id_filma]).fetchall()
        return naslov, leto, dolzina, ocena, zanri, vloge


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
