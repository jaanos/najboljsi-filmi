from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.shortcuts import reverse

class Oseba(models.Model):
    ime = models.CharField(max_length=200, help_text="Ime in priimek osebe.")
    vloge = models.ManyToManyField('Vloga', through='Nastopanje', related_name='osebe')

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
    ocena = models.FloatField(help_text="Ocena filma od 1 do 10.", null=False, default=0)
    glasovi = models.IntegerField(help_text="Stevilo glasov za oceno.", null=False, default=0)
    metascore = models.FloatField(help_text="Metascore tega filma od 1 do 100.", null=True)
    zasluzek = models.IntegerField(help_text="Zaslužek v USD.", null=True)
    opis = models.TextField(help_text="Opis filma.")
    zanr = models.ManyToManyField(Zanr, help_text='Žanri tega filma', related_name='filmi')
    osebe = models.ManyToManyField(Oseba, through='Nastopanje', related_name='filmi')

    class Meta:
        verbose_name_plural = 'Filmi'

    def __str__(self):
        return "{}".format(self.naslov)


class Nastopanje(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='nastopanja')
    oseba = models.ForeignKey(Oseba, on_delete=models.CASCADE, related_name='nastopanja')
    vloga = models.ForeignKey(Vloga, on_delete=models.CASCADE, related_name='nastopanja')

    class Meta:
        verbose_name_plural = 'Nastopanja'

    def __str__(self):
        return "{} je v filmu '{}' imel vlogo '{}'.".format(self.oseba, self.film, self.vloga)


class FilmForm(ModelForm):
    class Meta:
        model = Film
        fields = [
            'naslov', 'dolzina', 'leto', 
            'zasluzek', 'opis', 'zanr']

    def clean_dolzina(self):
        dolzina = self.cleaned_data['dolzina']
        if dolzina < 30:
            raise ValidationError('Dolzina filma mora biti vsaj 30 min.')
        return dolzina

    def clean_naslov(self):
        naslov = self.cleaned_data['naslov']
        film = Film.objects.filter(naslov=naslov).first()  # film ali None
        if film:
            raise ValidationError(
                mark_safe('Film z naslovom &ldquo;{}&rdquo; '
                          '<a href="{}" target="_blank">ze obstaja</a>.'.format(
                              naslov, reverse('film', args=(film.pk,)))))
        return naslov

