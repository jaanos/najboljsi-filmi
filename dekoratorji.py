import sqlite3

conn = sqlite3.connect('filmi.db')
conn.execute('PRAGMA foreign_keys = ON')

def polepsaj(funkcija, dekorirana_funkcija):
    """
    Poskrbi za ustrezno ime in dokumentacijo dekorirane funkcije.
    """
    dekorirana_funkcija.__doc__ = funkcija.__doc__
    dekorirana_funkcija.__name__ = funkcija.__name__
    dekorirana_funkcija.__qualname__ = funkcija.__qualname__

def cursor(fun):
    """
    Dekorator, ki ustvari kurzor in ga poda dekorirani funkciji.

    Originalna funkcija je na voljo pod atributom nocursor
    """
    def funkcija(*largs, **kwargs):
        cur = conn.cursor()
        try:
            ret = fun(cur, *largs, **kwargs)
        finally:
            cur.close()
        return ret
    polepsaj(fun, funkcija)
    fun.__qualname__ += '.nocursor'
    funkcija.nocursor = fun
    return funkcija


def commit(fun):
    """
    Dekorator, ki ustvari kurzor, ga poda dekorirani funkciji,
    in nato zapiše spremembe v bazo.

    Originalna funkcija je na voljo pod atributom nocommit.
    """
    def funkcija(*largs, **kwargs):
        cur = conn.cursor()
        try:
            ret = fun(cur, *largs, **kwargs)
            conn.commit()
        finally:
            cur.close()
        return ret
    polepsaj(fun, funkcija)
    fun.__qualname__ += '.nocommit'
    funkcija.nocommit = fun
    return funkcija
