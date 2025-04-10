# Generated by Django 3.2.13 on 2022-07-12 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_productrate_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='dotykacka_id',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='historicalcategory',
            name='dotykacka_id',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='dotykacka_id',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='dotykacka_id',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
