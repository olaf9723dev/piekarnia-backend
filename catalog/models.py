from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from simple_history.models import HistoricalRecords
from core.models import Tag, DeliveryType
from places.models import Place
from django.db.models import F, Sum, FloatField, Avg

GROUP_TYPE = (
    (0, 'select'),
    (1, 'radio'),
    (2, 'checkbox'),
    (3, 'quantity')
)

UNITS = (
    (0, 'szt.'),
    (1, 'kg'),
    (2, 'kpl.'),
    (3, 'l')
)


class Category(models.Model):
    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'
    name = models.CharField(max_length=128, verbose_name="Nazwa")
    image = models.ImageField(null=True, blank=True, verbose_name="Obraz")
    is_enabled = models.BooleanField(default=True, verbose_name="Dostępny")
    parent = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Rodzic")
    dotykacka_id = models.CharField(max_length=64, null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} - {'dostępny' if self.is_enabled else 'niedostępny'}"

    @property
    def image_url(self):
        return self.image.url if self.image else ''


class VariantGroup(models.Model):
    name = models.CharField(max_length=128, verbose_name="Nazwa")
    group_type = models.IntegerField(choices=GROUP_TYPE, verbose_name="Typ grupy")
    max_selected_count = models.IntegerField(default=1, verbose_name="Maksymalna ilość")
    min_selected_count = models.IntegerField(default=1, verbose_name="Minimalna ilość")

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}"


class Variant(models.Model):
    name = models.CharField(max_length=128, verbose_name="Wariant")
    group = models.ForeignKey(VariantGroup, default="", on_delete=models.CASCADE, verbose_name="Grupa wariantów")
    extra_price = models.FloatField(default=0, verbose_name="Dopłata")

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} - {self.group.name} - {self.extra_price}"


class Product(models.Model):
    name = models.CharField(max_length=1024, verbose_name="Nazwa")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoria")
    net_price = models.FloatField(verbose_name="Cena netto", null=True, blank=True)
    vat_base = models.FloatField(verbose_name="VAT", null=True, blank=True)
    short_description = models.TextField(verbose_name="Krótki opis", blank=True, null=True)
    description = models.TextField(verbose_name="Opis", blank=True, null=True)
    is_promo = models.BooleanField(default=False, verbose_name="Promocja")
    is_new = models.BooleanField(default=False, verbose_name="Nowość")
    product_code = models.CharField(max_length=128, verbose_name="Kod produktu", default=0)
    similar_products = models.ManyToManyField("Product", blank=True, null=True, verbose_name="Podobne produkty")
    is_enabled = models.BooleanField(default=True, verbose_name="Dostępny")
    tags = models.ManyToManyField(Tag, blank=True, null=True, verbose_name="Tagi")
    available_delivery_types = models.ManyToManyField(DeliveryType, blank=True, null=True, verbose_name="Dostępne opcje dostawy")
    dotykacka_id = models.CharField(max_length=128, null=True, blank=True)
    nutrition = models.CharField(max_length=64, verbose_name="Wartości odżywcze", null=True, blank=True)
    fat = models.FloatField(verbose_name="Tłuszcze", null=True, blank=True)
    fatty_acids = models.FloatField(verbose_name="Kwasy tłuszczowe", null=True, blank=True)
    carbohydrates = models.FloatField(verbose_name="Węglowodany", null=True, blank=True)
    sugar = models.FloatField(verbose_name="Cukry", null=True, blank=True)
    protein = models.FloatField(verbose_name="Białko", null=True, blank=True)
    fiber = models.FloatField(verbose_name="Błonnik", null=True, blank=True)
    salt = models.FloatField(verbose_name="Sól", null=True, blank=True)

    history = HistoricalRecords()

    @property
    def avg_rate(self):
        try:
            return round(ProductRate.objects.filter(product_id=self.pk).aggregate(total=Avg('rate'))['total'], 1)
        except:
            return 0

    @property
    def main_image(self):
        return ProductImage.objects.filter(product_id=self.pk, is_primary=True)

    @property
    def gross_price(self):
        return self.net_price * (self.vat_base)

    def __str__(self):
        return f"{self.name} - {self.category.name} - {'dostępny' if self.is_enabled else 'niedostępny'}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Nazwa")
    variant = models.ManyToManyField(Variant, verbose_name="Wariant")
    extra_price = models.FloatField(verbose_name="Dodatkowa opłata", null=True, blank=True)
    use_custom_stock = models.BooleanField(default=False, verbose_name="Ilość sztuk??")
    stock = models.FloatField(verbose_name="Ilość sztuk", null=True, blank=True)
    unit = models.IntegerField(choices=UNITS, verbose_name="Jednostka", default=0)
    delivery_time = models.FloatField(verbose_name="Czas dostawy", null=True, blank=True)
    image = models.ImageField(null=True, blank=True, verbose_name="Obraz")
    weight = models.FloatField(default=0, verbose_name="Waga", null=True, blank=True)
    is_enabled = models.BooleanField(default=True, verbose_name="Dostępny")

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.product.name} - {', '.join([variant.name for variant in self.variant.all()])} - {'dostępny' if self.is_enabled else 'niedostępny'}"

    def unit_name(self):
        return self.get_unit_display()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produkt")
    image = models.ImageField(verbose_name="Obraz", null=True, blank=True)
    is_primary = models.BooleanField(default=False, verbose_name="Pierwszy")
    order = models.IntegerField(default=0, verbose_name="Kolejność")

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.order} : {self.product.name} - {self.is_primary}"


class ProductDescriptionSection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produkt")
    name = models.CharField(max_length=1024, verbose_name="Nazwa")
    content = models.TextField(verbose_name="Opis")

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class ProductStatistic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produkt")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Użytkownik")
    date = models.DateTimeField(verbose_name="Data")

    def __str__(self):
        return f"{self.product.name} - {self.date} - {self.user}"


class ProductRate(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produkt")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Użytkownik")
    rate = models.FloatField(verbose_name="Ocena")
    date = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    comment = models.TextField(verbose_name="Komentarz")

    def __str__(self):
        return f"{self.product.name} - {self.rate}"


class ProductInPlace(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produkt")
    variant = models.ManyToManyField(ProductVariant, verbose_name="Wariant produktu")
    place = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name="Lokal")
    custom_price = models.FloatField(default=0, verbose_name="Cena")

    @property
    def price(self):
        return self.custom_price if self.custom_price else self.product.gross_price

    def __str__(self):
        return f"{self.product.name} - {self.place.name}"


class CategoryInPlace(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
