# Generated by Django 3.2.13 on 2022-06-08 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20220608_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardproductvariant',
            name='product',
        ),
    ]
