# Generated by Django 4.1.3 on 2022-11-24 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phones', '0004_alter_phone_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='image',
            field=models.URLField(blank=True),
        ),
    ]
