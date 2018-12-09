import modeli


MAX_REZULTATOV_ISKANJA = 15


def izberi_moznost(moznosti):
    """
    Funkcija, ki izpiše seznam možnosti in vrne indeks izbrane možnosti.

    Če na voljo ni nobene možnosti, izpiše opozorilo in vrne None.
    Če je na voljo samo ena možnost, vrne 0.

    >>> izberi_moznost(['jabolko', 'hruška', 'stol'])
    1) jabolko
    2) hruška
    3) stol
    Vnesite izbiro > 2
    1
    >>> izberi_moznost([])
    >>> izberi_moznost(['jabolko'])
    0
    """

    if len(moznosti) == 0:
        return
    elif len(moznosti) == 1:
        return 0
    else:
        for i, moznost in enumerate(moznosti, 1):
            print('{}) {}'.format(i, moznost))

        st_moznosti = len(moznosti)
        while True:
            izbira = input('Vnesite izbiro > ')
            if not izbira.isdigit():
                print('NAPAKA: vnesti morate število')
            else:
                n = int(izbira)
                if 1 <= n <= st_moznosti:
                    return n - 1
                else:
                    print('NAPAKA: vnesti morate število med 1 in {}!'.format(
                        st_moznosti))


def izberi_film():
    niz = input('Vnesite del naslova filma > ')
    idji_filmov = modeli.poisci_filme(niz)
    moznosti = [
        '{} ({})'.format(naslov, leto) for _, naslov, leto in modeli.podatki_filmov(idji_filmov)
    ]
    izbira = izberi_moznost(moznosti)
    return None if izbira is None else idji_filmov[izbira]


def izberi_osebo():
    niz = input('Vnesite del imena osebe > ')
    idji_oseb = modeli.poisci_osebe(niz)
    moznosti = [
        ime for _, ime in modeli.podatki_oseb(idji_oseb)
    ]
    izbira = izberi_moznost(moznosti)
    return None if izbira is None else idji_oseb[izbira]


def izberi_vlogo():
    vloge = modeli.mozne_vloge()
    moznosti = [
        naziv for _, naziv in vloge
    ]
    izbira = izberi_moznost(moznosti)
    id_vloge, _ = vloge[izbira]
    return id_vloge


def prikazi_podatke_filma():
    id_filma = izberi_film()
    if id_filma is None:
        print('Noben film ne ustreza iskalnemu nizu.')
    else:
        naslov, leto, dolzina, ocena, zanri, vloge = modeli.podatki_filma(id_filma)
        reziserji = modeli.podatki_oseb([id_osebe for (id_osebe, vloga) in vloge if vloga == 'reziser'])
        imena_reziserjev = [ime for (_, ime) in reziserji]
        igralci = modeli.podatki_oseb([id_osebe for (id_osebe, vloga) in vloge if vloga == 'igralec'])
        imena_igralcev = [ime for (_, ime) in igralci]

        print('{} ({})'.format(naslov, leto))
        print('  dolžina: {} min'.format(dolzina))
        print('  ocena: {}/10'.format(ocena))
        print('  žanri: {}'.format(', '.join(zanri)))
        if len(imena_reziserjev) == 1:
            print('  režiser: {}'.format(imena_reziserjev[0]))
        elif len(imena_reziserjev) > 1:
            print('  režiserji: {}'.format(', '.join(imena_reziserjev)))
        if len(imena_igralcev) == 1:
            print('  igra: {}'.format(imena_igralcev[0]))
        elif len(imena_igralcev) > 1:
            print('  igrajo: {}'.format(', '.join(imena_igralcev)))


def prikazi_podatke_osebe():
    id_osebe = izberi_osebo()
    if id_osebe is None:
        print('Nobena oseba ne ustreza iskalnemu nizu.')
    else:
        ime, vloge = modeli.podatki_osebe(id_osebe)
        naslovi_filmov = {
            id_filma: '{} ({})'.format(naslov, leto)
            for id_filma, naslov, leto
            in modeli.podatki_filmov([id_filma for id_filma, _ in vloge])
        }

        print(ime)
        for id_filma, vloga in vloge:
            print('  {} - {}'.format(naslovi_filmov[id_filma], vloga))


def dodaj_vlogo():
    id_osebe = izberi_osebo()
    id_filma = izberi_film()
    id_vloge = izberi_vlogo()
    modeli.dodaj_vlogo(id_osebe, id_filma, id_vloge)
    print('Vloga je uspešno dodana.')

def prikazi_najboljse_filme_desetletja():
    # TODO: preveri veljavnost vnosa števila
    leto = int(input('Vnesite leto iz želenega desetletja > '))
    desetletje, najboljsi_filmi = modeli.najboljsi_filmi_desetletja(leto)

    print('V obdobju {} – {} so bili najboljši filmi:'.format(desetletje, desetletje + 9))
    for i, (naslov, leto, ocena) in enumerate(najboljsi_filmi, 1):
        print('{}. {} ({}), {}/10'.format(i, naslov, leto, ocena))

def pokazi_moznosti():
    print(50 * '-')
    izbira = izberi_moznost([
        'prikaži podatke filma',
        'prikaži podatke osebe',
        'dodaj vlogo osebe v filmu',
        'prikaži najboljše filme posameznega desetletja',
        'izhod',
    ])
    if izbira == 0:
        prikazi_podatke_filma()
    elif izbira == 1:
        prikazi_podatke_osebe()
    elif izbira == 2:
        dodaj_vlogo()
    elif izbira == 3:
        prikazi_najboljse_filme_desetletja()
    elif izbira == 4:
        print('Nasvidenje!')
        exit()
        


def main():
    print('Pozdravljeni v bazi najboljših filmov!')
    while True:
        pokazi_moznosti()


main()
