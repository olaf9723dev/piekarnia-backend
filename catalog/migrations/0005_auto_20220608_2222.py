# Generated by Django 3.2.13 on 2022-06-08 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20220608_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalvariant',
            name='group_temp2',
            field=models.ForeignKey(blank=True, db_constraint=False, default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='catalog.variantgroup'),
        ),
        migrations.AddField(
            model_name='variant',
            name='group_temp2',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.variantgroup'),
        ),
    ]
