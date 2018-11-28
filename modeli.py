import sqlite3

conn = sqlite3.connect('filmi.db')
conn.execute('PRAGMA foreign_keys = ON')

def commit(fun):
    """
    Dekorator, ki ustvari kurzor, ga poda dekorirani funkciji,
    in nato zapiše spremembe v bazo.

    Originalna funkcija je na voljo pod atributom nocommit.
    """
    def funkcija(*largs, **kwargs):
        ret = fun(conn.cursor(), *largs, **kwargs)
        conn.commit()
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