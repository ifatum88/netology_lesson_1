# Generated by Django 4.1.3 on 2022-12-02 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Scope',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
