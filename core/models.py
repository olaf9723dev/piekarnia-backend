from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords


class OrderStatus(models.Model):
    name = models.CharField(max_length=128)
    sent_notification = models.BooleanField(default=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} - {self.sent_notification}"


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DeliveryType(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    icon = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.price}"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.FloatField(default=0)
    birt_date = models.DateField(null=True, blank=True)
    telephone = models.CharField(max_length=16)
    notifications_enabled = models.BooleanField(default=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user.username} - {self.telephone}"


@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)
    else:
        try:
            instance.client.save()
        except:
            pass


class ClientAddress(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    address_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    address = models.CharField(max_length=1024)
    zip_code = models.CharField(max_length=6)
    city = models.CharField(max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=16)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} - {self.client.user.username}"


class ClientInvoiceData(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    nip = models.CharField(max_length=14)
    company_name = models.CharField(max_length=255)
    address = models.CharField(max_length=1024)
    zip_code = models.CharField(max_length=6)
    city = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} - {self.client.user.username}"


class PaymentType(models.Model):
    name = models.CharField(max_length=128)
    code_name = models.CharField(max_length=128)
    is_enabled = models.BooleanField(default=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} - {self.code_name} - {self.is_enabled}"

    def display_name(self):
        map_display = {
            'credit-card': 'Karta',
            'apple-pay': 'Apple-pay',
            'google-pay': 'Google-pay',
            'cash': 'Gotówka',
            'blik': 'BLIK',
            'przelewy24': 'Przelewy24',
            'collect': 'Płatność przy odbiorze'
        }
        return map_display[self.name]


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
