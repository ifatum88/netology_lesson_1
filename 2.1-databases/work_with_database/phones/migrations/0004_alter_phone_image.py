# Generated by Django 4.1.3 on 2022-11-24 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phones', '0003_phone_image_phone_lte_exists_phone_name_phone_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
