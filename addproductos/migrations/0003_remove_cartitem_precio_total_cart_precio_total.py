# Generated by Django 5.0.6 on 2024-05-20 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addproductos', '0002_cartitem_precio_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='precio_total',
        ),
        migrations.AddField(
            model_name='cart',
            name='precio_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]