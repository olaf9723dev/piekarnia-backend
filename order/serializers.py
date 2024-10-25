from django.contrib.auth.models import User
from rest_framework import serializers

from authentication.serializers import UserSerializer
from catalog.serializers import ProductSerializer, ProductVariantSerializer, ProductInPlaceSerializer
from core.serializers import ClientSerializer, DeliveryTypeSerializer, PaymentTypeSerializer, ClientAddressSerializer
from order.models import ClientCart, CartProduct, CardProductVariant, RepeatedDays, OrderRepeatability, IssueImage, \
    OrderIssue, OrderDetails, OrderInvoice, OrderIssueMessage, OrderIssueConversation


class ClientCartSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    createDate = serializers.DateTimeField(source='create_date')
    lastUpdateDate = serializers.DateTimeField(source='last_update_date')
    cartCount = serializers.IntegerField(source='cart_count')

    class Meta:
        model = ClientCart
        fields = ["id", "client", "createDate", "lastUpdateDate", 'cartCount']


class CartProductSerializer(serializers.ModelSerializer):
    cart = ClientCartSerializer(read_only=True)

    class Meta:
        model = CartProduct
        fields = ["id", "cart", "quantity", "promo"]


class CartProductVariantSerializer(serializers.ModelSerializer):
    cartProduct = CartProductSerializer(read_only=True, source='cart_product')
    variant = ProductInPlaceSerializer(read_only=True)
    selectedVariant = serializers.IntegerField(source='selected_variant')
    selectedProductVariant = ProductVariantSerializer(source='selected_product_variant')
    productPriceSum = serializers.FloatField(source='product_price_sum')

    class Meta:
        model = CardProductVariant
        fields = ["id", "cartProduct", "variant", "quantity", "extra_price", "place", "selectedVariant",
                  "selectedProductVariant", "productPriceSum"]


class OrderDetailsSerializer(serializers.ModelSerializer):
    products = CartProductVariantSerializer(many=True, read_only=True)
    client = ClientSerializer(read_only=True)
    deliveryType = DeliveryTypeSerializer(source='delivery_type')
    deliveryAddress = ClientAddressSerializer(read_only=True, source='delivery_address')
    paymentMethod = PaymentTypeSerializer(source='payment_method')
    isRepeated = serializers.BooleanField(source='is_repeated')
    status = serializers.IntegerField()
    statusName = serializers.CharField(source='status_name')
    paymentStatus = serializers.IntegerField(source='payment_status')
    paymentStatusName = serializers.CharField(source='payment_status_name')
    orderPrice = serializers.FloatField(source='order_price')
    hasInvoice = serializers.BooleanField(source='has_invoice')
    createDate = serializers.DateTimeField(source='create_date')
    notesForOrder = serializers.CharField(source='notes_for_order')
    orderId = serializers.CharField(source='order_id')
    deliveryDate = serializers.DateTimeField(allow_null=True, source='delivery_date')

    class Meta:
        model = OrderDetails
        fields = ['id', 'products', 'client', 'status', 'statusName', 'deliveryType', 'deliveryAddress',
                  'paymentMethod', 'paymentStatus', 'paymentStatusName', 'isRepeated', 'orderPrice', 'hasInvoice',
                  'createDate', 'notesForOrder', 'orderId', 'deliveryDate']


class OrderInvoiceSerializer(serializers.ModelSerializer):
    orders = OrderDetailsSerializer(read_only=True, many=True)
    netPrice = serializers.FloatField(source='net_price')
    grossPrice = serializers.FloatField(source='gross_price')
    createDate = serializers.DateTimeField(source='create_date')
    statusName = serializers.CharField(source='status_name')

    class Meta:
        model = OrderInvoice
        fields = ['id', 'orders', 'name', 'invoice', 'netPrice', 'grossPrice', 'createDate', 'status', 'statusName']


class RepeatedDaysSerializer(serializers.ModelSerializer):
    dayName = serializers.CharField(source='day_name')
    dayNumber = serializers.IntegerField(source='day_number')

    class Meta:
        model = RepeatedDays
        fields = ['id', 'dayName', 'dayNumber']


class OrderRepeatabilitySerializer(serializers.ModelSerializer):
    order = OrderDetailsSerializer(read_only=True)
    repeatedDays = RepeatedDaysSerializer(many=True, read_only=True, source='repeated_days')

    class Meta:
        model = OrderRepeatability
        fields = ['id', 'order', 'repeatedDays', 'frequency']


class IssueImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueImage
        fields = ['id', 'image']


class OrderIssueSerializer(serializers.ModelSerializer):
    order = OrderDetailsSerializer(read_only=True)
    issueType = serializers.CharField(source='issue_type_name')
    customIssueType = serializers.CharField(source='custom_issue_type')
    issueImages = IssueImageSerializer(many=True, read_only=True, source='issue_images')
    statusName = serializers.CharField(source='status_name')
    createDate = serializers.DateTimeField(source='create_date')

    class Meta:
        model = OrderIssue
        fields = ['id', 'order', 'issueType', 'customIssueType', 'description', 'issueImages', 'status', 'statusName',
                  'createDate']


class OrderIssueMessageSerializer(serializers.ModelSerializer):
    createDate = serializers.DateTimeField(source='create_date')

    class Meta:
        model = OrderIssueMessage
        fields = ['id', 'message', 'image', 'createDate', 'author']


class OrderIssueConversationSerializer(serializers.ModelSerializer):
    issue = OrderIssueSerializer()
    messages = OrderIssueMessageSerializer(many=True, read_only=True)

    class Meta:
        model = OrderIssueConversation
        fields = ['id', 'issue', 'messages']
