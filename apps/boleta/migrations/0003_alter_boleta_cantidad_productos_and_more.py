# Generated by Django 5.0.6 on 2024-06-30 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boleta', '0002_rename_total_boleta_precio_total_remove_boleta_cart_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boleta',
            name='cantidad_productos',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='boleta',
            name='productos',
            field=models.JSONField(),
        ),
    ]
