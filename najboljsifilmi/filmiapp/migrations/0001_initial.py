# Generated by Django 2.1.7 on 2019-02-22 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Oseba',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(help_text='Ime in priimek osebe.', max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Osebe',
            },
        ),
    ]