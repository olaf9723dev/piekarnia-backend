# Generated by Django 3.2.13 on 2022-06-27 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_orderdetails_order_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='products_quantity',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]
