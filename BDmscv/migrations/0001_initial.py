# Generated by Django 3.1.1 on 2020-10-08 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comunidad',
            fields=[
                ('cod_comunidad', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nom_comunidad', models.CharField(max_length=100, verbose_name='Nombre de la comunidad')),
                ('descrip', models.TextField(blank=True, max_length=500, null=True, verbose_name='Descripcion')),
                ('fecha_creacion', models.DateField(blank=True, null=True, verbose_name='Fecha de creacion')),
                ('hubi_comuni', models.CharField(blank=True, max_length=100, null=True, verbose_name='Hubicacion de la Comunidad ')),
                ('coor_comuni', models.CharField(blank=True, max_length=100, null=True, verbose_name='Coordenadas para google maps')),
                ('is_active', models.BooleanField(default=False, verbose_name='¿Esta activo?')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('cod_per', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Nombre de Usuario')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electronico')),
                ('Rut', models.CharField(max_length=100, unique=True)),
                ('nombre', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombres')),
                ('apellido', models.CharField(blank=True, max_length=200, null=True, verbose_name='Apellidos')),
                ('imgen', models.ImageField(blank=True, max_length=200, null=True, upload_to='perfil/', verbose_name='Imagen de Perfil')),
                ('fecha_nac', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('direccion', models.CharField(blank=True, max_length=200, null=True, verbose_name='Direccion')),
                ('usuario_activo', models.BooleanField(default=True)),
                ('usuario_admin', models.BooleanField(default=False)),
                ('cod_comunidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BDmscv.comunidad', verbose_name='Codigo de la Comunidad')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('cod_rol', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha_ele_rol', models.DateField(verbose_name='Cuando fue elegido')),
                ('fecha_ter_rol', models.DateField(blank=True, null=True)),
                ('cod_per', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BDmscv.usuario', verbose_name='Codigo de la persona')),
            ],
        ),
        migrations.CreateModel(
            name='item',
            fields=[
                ('cod_item', models.BigAutoField(primary_key=True, serialize=False)),
                ('nom_item', models.CharField(max_length=100, verbose_name='Nombre del item')),
                ('fecha_recib', models.DateField(blank=True, null=True, verbose_name='Fecha cuando se recibio el item')),
                ('img_item', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Imagen del item')),
                ('cod_comunidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BDmscv.comunidad', verbose_name='Codigo de la Comunidad')),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('cod_evento', models.BigAutoField(primary_key=True, serialize=False)),
                ('nom_evento', models.CharField(max_length=100, verbose_name='Nombre del evento')),
                ('hubi_eve', models.CharField(max_length=100, verbose_name='Direccion del evento')),
                ('coor_eve', models.IntegerField(blank=True, null=True, verbose_name='Coordenadas para google maps')),
                ('fecha_crea_eve', models.DateField(auto_now=True)),
                ('fecha_reali_eve', models.DateField(verbose_name='Cuando se va a realizar el evento')),
                ('cod_comunidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BDmscv.comunidad', verbose_name='Codigo de la Comunidad')),
            ],
        ),
    ]
