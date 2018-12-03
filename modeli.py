from dekoratorji import conn, cursor, commit

@cursor
def obstaja_baza(cur):
    """
    Vrne True, če baza že obstaja.
    """
    cur.execute("SELECT COUNT(*) FROM sqlite_master")
    return cur.fetchone() != (0, )

@cursor
def pridobi_konstante(cur):
    """
    Nastavi konstanti IGRALEC in REZISER, če baza obstaja.
    """
    global IGRALEC, REZISER
    if obstaja_baza():
        cur = conn.cursor()
        cur.execute("SELECT id FROM vloga WHERE naziv = 'igralec'")
        IGRALEC, = cur.fetchone()
        cur.execute("SELECT id FROM vloga WHERE naziv = 'reziser'")
        REZISER, = cur.fetchone()
        cur.close()

pridobi_konstante()

@cursor
def poisci_podatke(cur, id_filma):
    '''
    Vrne podatke o filmu z danim IDjem

    Če film ne obstaja, vrne None, sicer vrne nabor:
        naslov, leto, dolžina, ocena, žanri
    pri čemer so žanri predstavljeni s seznamom nizov.
    '''
    poizvedba = """
        SELECT naslov, leto, dolzina, ocena FROM film WHERE id = ?
    """
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
    """
    Vrne ID podanega žanra.

    Če žanr še ne obstaja, ga doda v bazo.
    """
    cur.execute("SELECT id FROM zanr WHERE naziv = ?", [zanr])
    vrstica = cur.fetchone()
    if vrstica is not None:
        return vrstica[0]
    cur.execute("INSERT INTO zanr (naziv) VALUES (?)", [zanr])
    return cur.lastrowid

@commit
def id_osebe(cur, oseba):
    """
    Vrne ID podane osebe.

    Če oseba še ne obstaja, jo doda v bazo.
    """
    cur.execute("SELECT id FROM oseba WHERE ime = ?", [oseba])
    vrstica = cur.fetchone()
    if vrstica is not None:
        return vrstica[0]
    cur.execute("INSERT INTO oseba (ime) VALUES (?)", [oseba])
    return cur.lastrowid

@commit
def dodaj_film(cur, id, naslov, dolzina, leto, ocena, metascore,
               glasovi, zasluzek, opis, zanri=[], igralci=[],
               reziserji=[]):
    """
    V bazo doda film ter podatke o njegovih žanrih, igralcih in režiserjih.
    """
    cur.execute("""
        INSERT INTO film (id, naslov, dolzina, leto, ocena,
                          metascore, glasovi, zasluzek, opis)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [id, naslov, dolzina, leto, ocena,
          metascore, glasovi, zasluzek, opis])
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
