# Generated by Django 4.1.3 on 2022-11-24 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phones', '0002_phone_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='image',
            field=models.ImageField(default=None, upload_to=''),
        ),
        migrations.AddField(
            model_name='phone',
            name='lte_exists',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='phone',
            name='name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='phone',
            name='price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='phone',
            name='release_date',
            field=models.DateField(default='1900-01-01'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='slug',
            field=models.SlugField(),
        ),
    ]
