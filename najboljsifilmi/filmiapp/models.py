from django.db import models

class Oseba(models.Model):
    ime = models.CharField(max_length=200, help_text="Ime in priimek osebe.")

    class Meta:
        verbose_name_plural = 'Osebe'

    def __str__(self):
        return "{}".format(self.ime)

class Vloga(models.Model):
    naziv = models.CharField(max_length=200, help_text="Naziv vloge.")

    class Meta:
        verbose_name_plural = 'Vloge'

    def __str__(self):
        return "{}".format(self.naziv)


class Zanr(models.Model):
    naziv = models.CharField(max_length=200, help_text="Naziv žanra.")

    class Meta:
        verbose_name = 'Žanr'
        verbose_name_plural = 'Žanri'

    def __str__(self):
        return "{}".format(self.naziv)

class Film(models.Model):
    naslov = models.CharField(max_length=200, help_text="Naslov filma.")
    dolzina = models.IntegerField(help_text="Dolžina filma v minutah.")
    leto = models.PositiveSmallIntegerField(help_text="Leto premiere filma.")
    ocena = models.FloatField(help_text="Ocena filma od 1 do 10.", null=True)
    glasovi = models.IntegerField(help_text="Stevilo glasov za oceno.", null=True)
    metascore = models.FloatField(help_text="Metascore tega filma od 1 do 100.", null=True)
    zasluzek = models.IntegerField(help_text="Zaslužek v USD.", null=True)
    opis = models.TextField(help_text="Opis filma.")
    zanr = models.ManyToManyField(Zanr, help_text='Žanri tega filma')

    class Meta:
        verbose_name_plural = 'Filmi'

    def __str__(self):
        return "{}".format(self.naslov)


class Nastopanje(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    oseba = models.ForeignKey(Oseba, on_delete=models.CASCADE)
    vloga = models.ForeignKey(Vloga, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Nastopanja'

    def __str__(self):
        return "{} je v filmu '{}' imel vlogo '{}'.".format(self.oseba, self.film, self.vloga)
