# Generated by Django 3.1.1 on 2020-09-24 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evento',
            name='cod_comunidad',
        ),
        migrations.RemoveField(
            model_name='item',
            name='cod_comunidad',
        ),
        migrations.RemoveField(
            model_name='rol',
            name='cod_per',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='cod_comunidad',
        ),
        migrations.DeleteModel(
            name='Comunidad',
        ),
        migrations.DeleteModel(
            name='Evento',
        ),
        migrations.DeleteModel(
            name='item',
        ),
        migrations.DeleteModel(
            name='Rol',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
