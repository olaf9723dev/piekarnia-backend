# Generated by Django 3.2.13 on 2022-07-04 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0025_alter_orderrepeatability_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderissue',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='order.orderdetails'),
        ),
    ]
