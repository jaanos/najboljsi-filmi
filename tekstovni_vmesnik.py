import modeli

def izpisi_podatke(id_filma):
    podatki_filma = modeli.poisci_podatke(id_filma)
    if podatki_filma is None:
        print('Filma s tem IDjem ni')
    else:
        naslov, leto, dolzina, ocena, zanri = podatki_filma
        print('{} ({})'.format(naslov, leto))
        print('  dolžina: {} min'.format(dolzina))
        print('  ocena: {}/10'.format(ocena))
        print('  žanri: {}'.format(', '.join(zanri)))


print('Dober dan! Jaz ti bom dajal podatke o filmih.')
while True:
    id_filma = input('Vnesi ID filma: ')
    izpisi_podatke(id_filma)
