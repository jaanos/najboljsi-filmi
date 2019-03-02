"""
Napolni bazo s podatki, ki so dani v mapi podatki.

Pozeni kot

python manage.py shell -c "from filmiapp.napolni_bazo import main; main()"
"""

from filmiapp.models import *
import csv

from django.db import transaction


def main():
    # izbrisemo vse objekte
    Oseba.objects.all().delete()
    Film.objects.all().delete()
    Vloga.objects.all().delete()
    Zanr.objects.all().delete()
    Nastopanje.objects.all().delete()

    OSEBE_CSV = "podatki/oseba.csv"
    FILMI_CSV = "podatki/film.csv"
    VLOGA_CSV = "podatki/vloge.csv"
    ZANRI_CSV = "podatki/zanri.csv"

    print("Procesiram osebe ...")
    osebe = {}
    with open(OSEBE_CSV, encoding='utf-8') as f:
        f.readline()
        reader = csv.reader(f)

        for line in reader:
            pk, ime = line
            pk = int(pk)
            osebe[pk] = Oseba(ime=ime)

    with transaction.atomic():
        for o in osebe.values():
            o.save()

    print("Shranil {} oseb".format(len(osebe)))

    print("Procesiram filme ...")
    filmi = {}
    with open(FILMI_CSV, encoding='utf-8') as f:
        f.readline()
        reader = csv.reader(f)
        for line in reader:
            pk, naslov, dolzina, leto, ocena, metascore, glasovi, zasluzek, opis = line
            pk = int(pk)

            fl = Film(naslov=naslov, 
                      dolzina=int(dolzina),
                      leto=int(leto),
                      ocena=float(ocena),
                      glasovi=int(glasovi),
                      opis=opis)
            if metascore:
                fl.metascore = int(metascore)
            if zasluzek:
                fl.zasluzek = int(zasluzek)

            filmi[pk] = fl

    with transaction.atomic():
        for f in filmi.values():
            f.save()

    print("Shranil {} filmov".format(len(filmi)))

    print("Procesiram vloge ...")
    nastopanja = []
    with open(VLOGA_CSV, encoding='utf-8') as f:
        f.readline()
        reader = csv.reader(f)

        for line in reader:
            film_id, oseba_id, vloga = line
            film_id = int(film_id)
            oseba_id = int(oseba_id)
            
            V, _ = Vloga.objects.get_or_create(naziv=vloga)

            n = Nastopanje(oseba_id=osebe[oseba_id].pk,
                           film_id=filmi[film_id].pk,
                           vloga=V)

            nastopanja.append(n)

    Nastopanje.objects.bulk_create(nastopanja)
    print("Shranil {} nastopanj".format(len(nastopanja)))

    print("Procesiram zanre ...")
    povezave = []
    vmesni_model = Zanr.film_set.through
    with open(ZANRI_CSV, encoding='utf-8') as f:
        f.readline()
        reader = csv.reader(f)

        for line in reader:
            film_id, zanr = line
            film_id = int(film_id)
            
            Z, _ = Zanr.objects.get_or_create(naziv=zanr)
            povezave.append(vmesni_model(film=filmi[film_id], zanr=Z))

    vmesni_model.objects.bulk_create(povezave)
    print("Shranil {} povezav".format(len(povezave)))

