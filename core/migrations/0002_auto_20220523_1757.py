# Generated by Django 3.2.13 on 2022-05-23 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientaddress',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicalclientaddress',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
