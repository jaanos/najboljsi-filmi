import sqlite3

conn = sqlite3.connect('filmi.db')
conn.execute('PRAGMA foreign_keys = ON')

IGRALEC = None
REZISER = None

def obstaja_baza():
    cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
    return cur.fetchone() != (0, )

def pridobi_konstante():
    global IGRALEC, REZISER
    if obstaja_baza():
        cur = conn.cursor()
        cur.execute("SELECT id FROM vloga WHERE naziv = 'igralec'")
        IGRALEC, = cur.fetchone()
        cur.execute("SELECT id FROM vloga WHERE naziv = 'reziser'")
        REZISER, = cur.fetchone()
        cur.close()

pridobi_konstante()

def commit(fun):
    """
    Dekorator, ki ustvari kurzor, ga poda dekorirani funkciji,
    in nato zapiše spremembe v bazo.

    Originalna funkcija je na voljo pod atributom nocommit.
    """
    def funkcija(*largs, **kwargs):
        cur = conn.cursor()
        ret = fun(cur, *largs, **kwargs)
        conn.commit()
        cur.close()
        return ret
    funkcija.__doc__ = fun.__doc__
    funkcija.__name__ = fun.__name__
    funkcija.__qualname__ = fun.__qualname__
    fun.__qualname__ += '.nocommit'
    funkcija.nocommit = fun
    return funkcija


def poisci_podatke(id_filma):
    '''
    Vrne podatke o filmu z danim IDjem

    Če film ne obstaja, vrne None, sicer vrne nabor:
        naslov, leto, dolžina, ocena, žanri
    pri čemer so žanri predstavljeni s seznamom nizov.
    '''
    poizvedba = """
        SELECT naslov, leto, dolzina, ocena FROM film WHERE id = ?
    """
    cur = conn.cursor()
    cur.execute(poizvedba, [id_filma])
    osnovni_podatki = cur.fetchone()
    if osnovni_podatki is None:
        return None
    else:
        naslov, leto, dolzina, ocena = osnovni_podatki
        poizvedba_za_zanre = """
            SELECT zanr.naziv FROM zanr JOIN pripada ON zanr.id = pripada.zanr WHERE pripada.film = ?
        """
        cur.execute(poizvedba_za_zanre, [id_filma])
        zanri = [vrstica[0] for vrstica in cur.fetchall()]
        return naslov, leto, dolzina, ocena, zanri

@commit
def id_zanra(cur, zanr):
    cur.execute("SELECT id FROM zanr WHERE naziv = ?", [zanr])
    vrstica = cur.fetchone()
    if vrstica is not None:
        return vrstica[0]
    cur.execute("INSERT INTO zanr (naziv) VALUES (?)", [zanr])
    return cur.lastrowid

@commit
def id_osebe(cur, oseba):
    cur.execute("SELECT id FROM oseba WHERE ime = ?", [oseba])
    vrstica = cur.fetchone()
    if vrstica is not None:
        return vrstica[0]
    cur.execute("INSERT INTO oseba (ime) VALUES (?)", [oseba])
    return cur.lastrowid

@commit
def dodaj_film(cur, id, naslov, dolzina, leto, metascore,
               glasovi, zasluzek, opis, zanri=[], igralci=[],
               reziserji=[]):
    cur.execute("""
        INSERT INTO film (id, naslov, dolzina, leto, metascore,
                          glasovi, zasluzek, opis) VALUES
                         (?, ?, ?, ?, ?, ?, ?, ?)
    """, [id, naslov, dolzina, leto, metascore,
          glasovi, zasluzek, opis])
    for zanr in zanri:
        cur.execute("INSERT INTO pripada (film, zanr) VALUES (?, ?)",
                    [id, id_zanra.nocommit(cur, zanr)])
    for igralec in igralci:
        cur.execute("""
            INSERT INTO nastopa (film, oseba, vloga)
            VALUES (?, ?, ?)
        """, (id, id_osebe.nocommit(cur, igralec), IGRALEC))
    for reziser in reziserji:
        cur.execute("""
            INSERT INTO nastopa (film, oseba, vloga)
            VALUES (?, ?, ?)
        """, (id, id_osebe.nocommit(cur, reziser), REZISER))
