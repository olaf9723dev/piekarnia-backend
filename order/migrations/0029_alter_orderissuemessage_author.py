# Generated by Django 3.2.13 on 2022-07-05 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0028_auto_20220705_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderissuemessage',
            name='author',
            field=models.CharField(max_length=12),
        ),
    ]
