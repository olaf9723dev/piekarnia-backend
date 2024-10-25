# Generated by Django 3.2.13 on 2022-06-20 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20220609_1255'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0008_auto_20220613_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproductvariant',
            name='variant',
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Obraz'),
        ),
        migrations.AlterField(
            model_name='category',
            name='is_enabled',
            field=models.BooleanField(default=True, verbose_name='Dostępny'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Rodzic'),
        ),
        migrations.AlterField(
            model_name='historicalcategory',
            name='image',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Obraz'),
        ),
        migrations.AlterField(
            model_name='historicalcategory',
            name='is_enabled',
            field=models.BooleanField(default=True, verbose_name='Dostępny'),
        ),
        migrations.AlterField(
            model_name='historicalcategory',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='historicalcategory',
            name='parent',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='catalog.category', verbose_name='Rodzic'),
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='category',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='catalog.category', verbose_name='Kategoria'),
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='description',
            field=models.TextField(verbose_name='Opis'),
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='is_enabled',
            field=models.BooleanField(default=True, verbose_name='Dostępny'),
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='is_new',
            field=models.BooleanField(default=False, verbose_name='Nowość'),
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='is_promo',
            field=models.BooleanField(default=False, verbose_name='Promocja'),
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='name',
            field=models.CharField(max_length=1024, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='net_price',
            field=models.FloatField(verbose_name='Cena netto'),
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='product_code',
            field=models.CharField(max_length=128, verbose_name='Kod produktu'),
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='short_description',
            field=models.TextField(verbose_name='Krótki opis'),
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='vat_base',
            field=models.FloatField(verbose_name='VAT'),
        ),
        migrations.AlterField(
            model_name='historicalproductdescriptionsection',
            name='content',
            field=models.TextField(verbose_name='Opis'),
        ),
        migrations.AlterField(
            model_name='historicalproductdescriptionsection',
            name='name',
            field=models.CharField(max_length=1024, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='historicalproductdescriptionsection',
            name='product',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='catalog.product', verbose_name='Produkt'),
        ),
        migrations.AlterField(
            model_name='historicalproductimage',
            name='image',
            field=models.TextField(max_length=100, verbose_name='Obraz'),
        ),
        migrations.AlterField(
            model_name='historicalproductimage',
            name='is_primary',
            field=models.BooleanField(default=False, verbose_name='Pierwszy'),
        ),
        migrations.AlterField(
            model_name='historicalproductimage',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Kolejność'),
        ),
        migrations.AlterField(
            model_name='historicalproductimage',
            name='product',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='catalog.product', verbose_name='Produkt'),
        ),
        migrations.AlterField(
            model_name='historicalproductvariant',
            name='delivery_time',
            field=models.FloatField(verbose_name='Czas dostawy'),
        ),
        migrations.AlterField(
            model_name='historicalproductvariant',
            name='extra_price',
            field=models.FloatField(verbose_name='Dodatkowa opłata'),
        ),
        migrations.AlterField(
            model_name='historicalproductvariant',
            name='image',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Obraz'),
        ),
        migrations.AlterField(
            model_name='historicalproductvariant',
            name='is_enabled',
            field=models.BooleanField(default=True, verbose_name='Dostępny'),
        ),
        migrations.AlterField(
            model_name='historicalproductvariant',
            name='product',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='catalog.product', verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='historicalproductvariant',
            name='stock',
            field=models.FloatField(verbose_name='Ilość sztuk'),
        ),
        migrations.AlterField(
            model_name='historicalproductvariant',
            name='unit',
            field=models.IntegerField(choices=[(0, 'szt.'), (1, 'kg.'), (2, 'kpl.'), (3, 'l')], verbose_name='Jednostka'),
        ),
        migrations.AlterField(
            model_name='historicalproductvariant',
            name='use_custom_stock',
            field=models.BooleanField(default=False, verbose_name='Ilość sztuk??'),
        ),
        migrations.AlterField(
            model_name='historicalproductvariant',
            name='variant_group',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='catalog.variantgroup', verbose_name='Grupa wariantów'),
        ),
        migrations.AlterField(
            model_name='historicalproductvariant',
            name='weight',
            field=models.FloatField(default=0, verbose_name='Waga'),
        ),
        migrations.AlterField(
            model_name='historicalvariant',
            name='extra_price',
            field=models.FloatField(default=0, verbose_name='Dopłata'),
        ),
        migrations.AlterField(
            model_name='historicalvariant',
            name='group',
            field=models.ForeignKey(blank=True, db_constraint=False, default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='catalog.variantgroup', verbose_name='Grupa wariantów'),
        ),
        migrations.AlterField(
            model_name='historicalvariant',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Wariant'),
        ),
        migrations.AlterField(
            model_name='historicalvariantgroup',
            name='group_type',
            field=models.IntegerField(choices=[(0, 'select'), (1, 'radio'), (2, 'checkbox'), (3, 'quantity')], verbose_name='Typ grupy'),
        ),
        migrations.AlterField(
            model_name='historicalvariantgroup',
            name='max_selected_count',
            field=models.IntegerField(default=1, verbose_name='Maksymalna ilość'),
        ),
        migrations.AlterField(
            model_name='historicalvariantgroup',
            name='min_selected_count',
            field=models.IntegerField(default=1, verbose_name='Minimalna ilość'),
        ),
        migrations.AlterField(
            model_name='historicalvariantgroup',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='product',
            name='available_delivery_types',
            field=models.ManyToManyField(blank=True, null=True, to='core.DeliveryType', verbose_name='Dostępne opcje dostawy'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Kategoria'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Opis'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_enabled',
            field=models.BooleanField(default=True, verbose_name='Dostępny'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_new',
            field=models.BooleanField(default=False, verbose_name='Nowość'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_promo',
            field=models.BooleanField(default=False, verbose_name='Promocja'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=1024, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='product',
            name='net_price',
            field=models.FloatField(verbose_name='Cena netto'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(max_length=128, verbose_name='Kod produktu'),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=models.TextField(verbose_name='Krótki opis'),
        ),
        migrations.AlterField(
            model_name='product',
            name='similar_products',
            field=models.ManyToManyField(blank=True, null=True, to='catalog.Product', verbose_name='Podobne proodukty'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='core.Tag', verbose_name='Tagi'),
        ),
        migrations.AlterField(
            model_name='product',
            name='vat_base',
            field=models.FloatField(verbose_name='VAT'),
        ),
        migrations.AlterField(
            model_name='productdescriptionsection',
            name='content',
            field=models.TextField(verbose_name='Opis'),
        ),
        migrations.AlterField(
            model_name='productdescriptionsection',
            name='name',
            field=models.CharField(max_length=1024, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='productdescriptionsection',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Produkt'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='Obraz'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='is_primary',
            field=models.BooleanField(default=False, verbose_name='Pierwszy'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Kolejność'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Produkt'),
        ),
        migrations.AlterField(
            model_name='productrate',
            name='date',
            field=models.DateTimeField(verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='productrate',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Produkt'),
        ),
        migrations.AlterField(
            model_name='productrate',
            name='rate',
            field=models.FloatField(verbose_name='Ocena'),
        ),
        migrations.AlterField(
            model_name='productrate',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik'),
        ),
        migrations.AlterField(
            model_name='productstatistic',
            name='date',
            field=models.DateTimeField(verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='productstatistic',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Produkt'),
        ),
        migrations.AlterField(
            model_name='productstatistic',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='delivery_time',
            field=models.FloatField(verbose_name='Czas dostawy'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='extra_price',
            field=models.FloatField(verbose_name='Dodatkowa opłata'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Obraz'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='is_enabled',
            field=models.BooleanField(default=True, verbose_name='Dostępny'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='stock',
            field=models.FloatField(verbose_name='Ilość sztuk'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='unit',
            field=models.IntegerField(choices=[(0, 'szt.'), (1, 'kg.'), (2, 'kpl.'), (3, 'l')], verbose_name='Jednostka'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='use_custom_stock',
            field=models.BooleanField(default=False, verbose_name='Ilość sztuk??'),
        ),
        migrations.RemoveField(
            model_name='productvariant',
            name='variant',
        ),
        migrations.AddField(
            model_name='productvariant',
            name='variant',
            field=models.ManyToManyField(to='catalog.Variant', verbose_name='Wariant'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='variant_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.variantgroup', verbose_name='Grupa wariantów'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='weight',
            field=models.FloatField(default=0, verbose_name='Waga'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='extra_price',
            field=models.FloatField(default=0, verbose_name='Dopłata'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='group',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='catalog.variantgroup', verbose_name='Grupa wariantów'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Wariant'),
        ),
        migrations.AlterField(
            model_name='variantgroup',
            name='group_type',
            field=models.IntegerField(choices=[(0, 'select'), (1, 'radio'), (2, 'checkbox'), (3, 'quantity')], verbose_name='Typ grupy'),
        ),
        migrations.AlterField(
            model_name='variantgroup',
            name='max_selected_count',
            field=models.IntegerField(default=1, verbose_name='Maksymalna ilość'),
        ),
        migrations.AlterField(
            model_name='variantgroup',
            name='min_selected_count',
            field=models.IntegerField(default=1, verbose_name='Minimalna ilość'),
        ),
        migrations.AlterField(
            model_name='variantgroup',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Nazwa'),
        ),
    ]
