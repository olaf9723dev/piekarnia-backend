# Generated by Django 3.2.13 on 2022-06-28 17:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_orderdetails_products_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderissue',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderissue',
            name='issue_type',
            field=models.IntegerField(choices=[(0, 'Uszkodzony produkt'), (1, 'Problem z dostawą'), (2, 'Niepełne zamówienie'), (3, 'Błędne dane'), (4, 'Inne... (własne)')], default=0),
        ),
    ]
