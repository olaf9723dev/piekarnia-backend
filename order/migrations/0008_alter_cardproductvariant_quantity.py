# Generated by Django 3.2.13 on 2022-06-15 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_cardproductvariant_selected_variant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardproductvariant',
            name='quantity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
