import bottle
from bottle import get, post, run, template, request, redirect
import modeli


def url_filma(id):
    return '/film/{}/'.format(id)

@get('/')
def glavna_stran():
    desetletja = [
        (desetletje, '/najboljsi-filmi/{}/'.format(desetletje))
        for desetletje in modeli.mozna_desetletja()
    ]
    return template(
        'glavna_stran',
        desetletja=desetletja
    )

@get('/iskanje/')
def iskanje():
    niz = request.query.naslov
    idji_filmov = modeli.poisci_filme(niz)
    filmi = [(id, naslov, leto, '/film/{}/'.format(id)) for (id, naslov, leto) in modeli.podatki_filmov(idji_filmov)]
    return template(
        'rezultati_iskanja',
        niz=niz,
        filmi=filmi,
    )

@get('/film/<id_filma:int>/')
def podatki_filma(id_filma):
    naslov, leto, dolzina, ocena, zanri, vloge = modeli.podatki_filma(id_filma)
    reziserji = modeli.podatki_oseb([id_osebe for (id_osebe, vloga) in vloge if vloga == 'reziser'])
    igralci = modeli.podatki_oseb([id_osebe for (id_osebe, vloga) in vloge if vloga == 'igralec'])
    return template(
        'podatki_filma',
        naslov=naslov,
        leto=leto,
        dolzina=dolzina,
        ocena=ocena,
        zanri=zanri,
        reziserji=reziserji,
        igralci=igralci,
    )


@get('/najboljsi-filmi/')
@get('/najboljsi-filmi/<desetletje:int>/')
def najboljsi_filmi_desetletja(desetletje=2010):
    desetletje, najboljsi_filmi = modeli.najboljsi_filmi_desetletja(desetletje)
    return template(
        'najboljsi_filmi_desetletja',
        desetletje=desetletje,
        filmi=najboljsi_filmi,
    )

@get('/dodaj_film/')
def dodaj_film():
    zanri = modeli.seznam_zanrov()
    osebe = modeli.seznam_oseb()
    return template('dodaj_film',
                    naslov="",
                    dolzina="",
                    leto="",
                    ocena="",
                    metascore="",
                    glasovi="",
                    zasluzek="",
                    opis="",
                    zanri=[],
                    igralci=[],
                    reziserji=[],
                    vsi_zanri=zanri,
                    vse_osebe=osebe,
                    napaka=False)

@post('/dodaj_film/')
def dodajanje_filma():
    try:
        id = modeli.dodaj_film(naslov=request.forms.naslov,
                               dolzina=request.forms.dolzina,
                               leto=request.forms.leto,
                               ocena=request.forms.ocena,
                               metascore=request.forms.metascore,
                               glasovi=request.forms.glasovi,
                               zasluzek=request.forms.zasluzek,
                               opis=request.forms.opis,
                               zanri=request.forms.getall('zanri'),
                               igralci=request.forms.getall('igralci'),
                               reziserji=request.forms.getall('reziserji'))
    except:
        zanri = modeli.seznam_zanrov()
        osebe = modeli.seznam_oseb()
        return template('dodaj_film',
                        naslov=request.forms.naslov,
                        dolzina=request.forms.dolzina,
                        leto=request.forms.leto,
                        ocena=request.forms.ocena,
                        metascore=request.forms.metascore,
                        glasovi=request.forms.glasovi,
                        zasluzek=request.forms.zasluzek,
                        opis=request.forms.opis,
                        zanri=request.forms.getall('zanri'),
                        igralci=request.forms.getall('igralci'),
                        reziserji=request.forms.getall('reziserji'),
                        vsi_zanri=zanri,
                        vse_osebe=osebe,
                        napaka=True)
    redirect('/film/{}/'.format(id))

run(reloader=True, debug=True)
