# Generated by Django 3.2.13 on 2022-07-13 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0008_auto_20220712_1238'),
        ('catalog', '0015_auto_20220712_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinplace',
            name='custom_price',
            field=models.FloatField(default=0, verbose_name='Cena'),
        ),
        migrations.AlterField(
            model_name='productinplace',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.place', verbose_name='Lokal'),
        ),
        migrations.AlterField(
            model_name='productinplace',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Produkt'),
        ),
        migrations.AlterField(
            model_name='productinplace',
            name='variant',
            field=models.ManyToManyField(to='catalog.ProductVariant', verbose_name='Wariant produktu'),
        ),
    ]
