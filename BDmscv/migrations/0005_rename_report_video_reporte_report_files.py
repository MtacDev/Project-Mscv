# Generated by Django 3.2.3 on 2021-06-08 01:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BDmscv', '0004_auto_20210607_2058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reporte',
            old_name='report_video',
            new_name='report_files',
        ),
    ]