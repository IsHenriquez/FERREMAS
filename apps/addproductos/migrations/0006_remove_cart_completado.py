# Generated by Django 5.0.6 on 2024-06-30 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addproductos', '0005_cart_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='completado',
        ),
    ]
