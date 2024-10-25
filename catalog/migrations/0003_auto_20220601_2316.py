# Generated by Django 3.2.13 on 2022-06-01 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20220524_2223'),
        ('catalog', '0002_auto_20220528_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='available_delivery_types',
            field=models.ManyToManyField(blank=True, null=True, to='core.DeliveryType'),
        ),
        migrations.AlterField(
            model_name='product',
            name='similar_products',
            field=models.ManyToManyField(blank=True, null=True, to='catalog.Product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='core.Tag'),
        ),
    ]
