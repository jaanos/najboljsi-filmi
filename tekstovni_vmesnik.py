import sqlite3

conn = sqlite3.connect('filmi.db')

def izpisi_podatke(id_filma):
    poizvedba = '''
        SELECT naslov, leto, dolzina, ocena FROM film WHERE id = ?
    '''
    cur = conn.cursor()
    cur.execute(poizvedba, [id_filma])
    rezultat = cur.fetchone()
    if rezultat is None:
        print('Filma s tem IDjem ni')
    else:
        naslov, leto, dolzina, ocena = rezultat
        print('{} ({})'.format(naslov, leto))
        print('  dolžina: {} min'.format(dolzina))
        print('  ocena: {}/10'.format(ocena))

        poizvedba_za_zanre = '''
            SELECT zanr FROM zanr WHERE film = ?
        '''
        cur.execute(poizvedba_za_zanre, [id_filma])
        zanri = cur.fetchall()
        print('  žanri: {}'.format(', '.join(zanr[0] for zanr in zanri)))


print('Dober dan! Jaz ti bom dajal podatke o filmih.')
while True:
    id_filma = input('Vnesi ID filma: ')
    izpisi_podatke(id_filma)
