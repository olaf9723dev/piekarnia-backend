from rest_framework import serializers

from authentication.serializers import UserSerializer
from core.models import OrderStatus, Client, ClientAddress, ClientInvoiceData, PaymentType, DeliveryType, Notification


class OrderStatusSerializer(serializers.ModelSerializer):
    sentNotification = serializers.BooleanField(source='sent_notification')

    class Meta:
        model = OrderStatus
        fields = ["id", "name", "sentNotification"]


class DeliveryTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryType
        fields = ['id', 'name', 'price', 'icon']


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    birthDate = serializers.DateField(source='birt_date')
    notificationsEnabled = serializers.BooleanField(source='notifications_enabled')

    class Meta:
        model = Client
        fields = ["id", "user", "points", "birthDate", "telephone", "notificationsEnabled"]


class ClientAddressSerializer(serializers.ModelSerializer):
    # client = ClientSerializer()
    addressName = serializers.CharField(source='address_name')
    zipCode = serializers.CharField(source='zip_code')
    isDefault = serializers.BooleanField(source='is_default')
    phoneNumber = serializers.CharField(source='phone_number')

    class Meta:
        model = ClientAddress
        fields = ["id", "client_id", "addressName", "name", "surname", "address", "zipCode", "city", "latitude",
                  "longitude", "isDefault", 'phoneNumber', 'comment']


class ClientInvoiceDataSerializer(serializers.ModelSerializer):
    # client = ClientSerializer()
    clientId = serializers.IntegerField(source='client_id')
    companyName = serializers.CharField(source='company_name')
    zipCode = serializers.CharField(source='zip_code')
    isDefault = serializers.BooleanField(source='is_default')

    class Meta:
        model = ClientInvoiceData
        fields = ["id", "clientId", "name", "name", "nip", "companyName", "address", "zipCode",
                  "city", "isDefault"]


class PaymentTypeSerializer(serializers.ModelSerializer):
    codeName = serializers.CharField(source='code_name')
    isEnabled = serializers.BooleanField(source='is_enabled')
    displayName = serializers.CharField(source='display_name')

    class Meta:
        model = PaymentType
        fields = ["id", "name", "codeName", "isEnabled", "displayName"]


class NotificationSerializer(serializers.ModelSerializer):
    createDate = serializers.DateTimeField(source='create_date')
    user = UserSerializer()

    class Meta:
        model = Notification
        fields = ('pk', 'createDate', 'user', 'title', 'content')
