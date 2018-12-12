import bottle
from bottle import get, run, template
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

@get('/iskanje/<niz>/')
def iskanje(niz):
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

run(reloader=True, debug=True)
