# Generated by Django 3.2.13 on 2022-07-04 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0024_orderdetails_has_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrepeatability',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='order.orderdetails'),
        ),
    ]
