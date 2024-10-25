from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from catalog.models import Product, ProductVariant, ProductInPlace
from core.models import Client, DeliveryType, PaymentType, ClientAddress

ORDER_STATUS = (
    (0, 'oczekiwanie na płatność'),
    (1, 'opłacono'),
    (2, 'w realizacji'),
    (3, 'zrealizowane'),
    (4, 'gotowe do odbioru'),
    (5, 'wydano'),
)

ISSUE_TYPE = (
    (1, 'Uszkodzony produkt'),
    (2, 'Problem z dostawą'),
    (3, 'Niepełne zamówienie'),
    (4, 'Błędne dane'),
    (5, 'Inne... (własne)')
)

PAYMENT_STATUS = (
    (0, 'oczekuje na płatność'),
    (1, 'odrzucono'),
    (2, 'opłacono'),
    (3, 'anulowano'),
    (4, 'płatność przy odbiorze')
)

ISSUE_STATUS = (
    (0, 'oczekuje na rozpatrzenie'),
    (1, 'rozpatrzone')
)

INVOICE_STATUS = (
    (0, 'zlecono wystawienie'),
    (1, 'wystawiono')
)


class ClientCart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    is_closed = models.BooleanField(default=False)

    @property
    def cart_count(self):
        if CardProductVariant.objects.filter(cart_product__cart_id=self.pk).exists():
            return int(CardProductVariant.objects.filter(cart_product__cart_id=self.pk).aggregate(total=Sum('quantity'))['total'])
        else:
            return 0

    def __str__(self):
        return f"{self.client.user.username} - {self.last_update_date}"


class CartProduct(models.Model):
    cart = models.ForeignKey(ClientCart, on_delete=models.CASCADE)
    promo = models.FloatField(default=0)

    @property
    def quantity(self):
        return CardProductVariant.objects.filter(cart_product__cart_id=self.cart.pk).aggregate(total=Sum('quantity'))['total']

    @property
    def standard_price(self):
        return sum([element.price for element in self.cardproductvariant_set.all()])

    @property
    def promo_price(self):
        return self.standard_price * (1 - self.promo)

    def __str__(self):
        return f"{self.cart} : {self.quantity}"


class CardProductVariant(models.Model):
    cart_product = models.ForeignKey(CartProduct, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductInPlace, on_delete=models.CASCADE)
    selected_variant = models.IntegerField()
    quantity = models.FloatField(null=True, blank=True)

    @property
    def extra_price(self):
        return round(ProductVariant.objects.get(pk=self.selected_variant).extra_price, 2)

    @property
    def selected_product_variant(self):
        return ProductVariant.objects.get(pk=self.selected_variant)

    @property
    def place(self):
        return ProductInPlace.objects.get(pk=self.variant_id).place_id

    @property
    def product_price_sum(self):
        product = CardProductVariant.objects.get(pk=self.pk)
        price_sum = product.quantity * (product.variant.price + self.extra_price)
        return round(price_sum, 2)

    def __str__(self):
        return f"{self.variant.product.name} - {' + '.join([variant.name for variant in self.selected_product_variant.variant.all()])} x {self.quantity}"


class OrderDetails(models.Model):
    products = models.ManyToManyField(CardProductVariant)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    status = models.IntegerField(choices=ORDER_STATUS, default=0)
    delivery_type = models.ForeignKey(DeliveryType, on_delete=models.DO_NOTHING)
    delivery_address = models.ForeignKey(ClientAddress, on_delete=models.DO_NOTHING, null=True, blank=True)
    delivery_date = models.DateTimeField(default=None, null=True)
    payment_method = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING)
    payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=0)
    is_repeated = models.BooleanField(default=False)
    order_price = models.FloatField()
    has_invoice = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    notes_for_order = models.TextField(default='')
    order_id = models.CharField(max_length=128)

    @property
    def status_name(self):
        return self.get_status_display()

    @property
    def payment_status_name(self):
        return self.get_payment_status_display()


class OrderInvoice(models.Model):
    orders = models.ManyToManyField(OrderDetails)
    name = models.CharField(max_length=128, null=True, blank=True)
    invoice = models.FileField(null=True, blank=True)
    net_price = models.FloatField(null=True, blank=True)
    gross_price = models.FloatField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=INVOICE_STATUS, default=0)

    @property
    def status_name(self):
        return self.get_status_display()


class IssueImage(models.Model):
    image = models.ImageField()


class OrderIssue(models.Model):
    order = models.ForeignKey(OrderDetails, on_delete=models.CASCADE)
    issue_type = models.IntegerField(choices=ISSUE_TYPE, default=0)
    custom_issue_type = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(verbose_name="Opis zgłoszenia")
    issue_images = models.ManyToManyField(IssueImage)
    status = models.IntegerField(choices=ISSUE_STATUS, default=0)
    create_date = models.DateTimeField(auto_now_add=True)

    @property
    def status_name(self):
        return self.get_status_display()

    @property
    def issue_type_name(self):
        return self.get_issue_type_display()


class RepeatedDays(models.Model):
    day_name = models.CharField(max_length=32)
    day_number = models.IntegerField()


class OrderRepeatability(models.Model):
    order = models.ForeignKey(OrderDetails, on_delete=models.CASCADE)
    repeated_days = models.ManyToManyField(RepeatedDays, null=True, blank=True)
    frequency = models.CharField(max_length=64, null=True, blank=True)


class OrderIssueMessage(models.Model):
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=12)


class OrderIssueConversation(models.Model):
    issue = models.ForeignKey(OrderIssue, on_delete=models.CASCADE)
    messages = models.ManyToManyField(OrderIssueMessage)
