# Generated by Django 5.2 on 2025-04-15 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseDatos', '0005_detalleventa_cantidad_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='url',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]
