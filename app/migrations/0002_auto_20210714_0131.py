# Generated by Django 3.2.5 on 2021-07-13 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Game',
            new_name='Sport',
        ),
        migrations.RenameField(
            model_name='tournament',
            old_name='game',
            new_name='sport',
        ),
    ]