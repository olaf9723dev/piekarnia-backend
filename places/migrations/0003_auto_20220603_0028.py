# Generated by Django 3.2.13 on 2022-06-02 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_auto_20220528_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalopeninghours',
            name='end_time',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='historicalopeninghours',
            name='start_time',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='end_time',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='start_time',
            field=models.TimeField(default='00:00'),
        ),
    ]
