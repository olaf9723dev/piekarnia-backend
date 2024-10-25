# Generated by Django 3.2.13 on 2022-10-03 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0022_auto_20221003_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproduct',
            name='nutrition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='nutrition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalproductvariant',
            name='unit',
            field=models.IntegerField(choices=[(0, 'szt.'), (1, 'kg'), (2, 'kpl.'), (3, 'l')], default=0, verbose_name='Jednostka'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='unit',
            field=models.IntegerField(choices=[(0, 'szt.'), (1, 'kg'), (2, 'kpl.'), (3, 'l')], default=0, verbose_name='Jednostka'),
        ),
    ]
