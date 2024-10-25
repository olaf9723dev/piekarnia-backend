import datetime
import json

import pytz
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q

from catalog.models import Category, ProductInPlace, ProductImage, ProductVariant, ProductDescriptionSection, \
    ProductRate, CategoryInPlace
from catalog.serializers import CategorySerializer, ProductInPlaceSerializer, ProductImageSerializer, \
    ProductDescriptionSectionSerializer, ProductRateSerializer, CategoryInPlaceSerializer
from order.models import CardProductVariant, ClientCart, CartProduct, OrderDetails, OrderRepeatability, RepeatedDays, \
    OrderInvoice, OrderIssue, OrderIssueMessage, OrderIssueConversation, IssueImage
from order.serializers import CartProductVariantSerializer, ClientCartSerializer, OrderDetailsSerializer, \
    OrderInvoiceSerializer, OrderRepeatabilitySerializer, OrderIssueSerializer, \
    OrderIssueMessageSerializer, OrderIssueConversationSerializer
from places.models import Place
from places.serializers import PlaceSerializer
from .models import ClientAddress, Client, ClientInvoiceData, PaymentType, DeliveryType, Notification
from .serializers import ClientAddressSerializer, ClientInvoiceDataSerializer, ClientSerializer, DeliveryTypeSerializer, \
    NotificationSerializer

# Create your views here.
from .tools import create_notification, CustomPagination


class Addresses(viewsets.ModelViewSet):
    serializer_class = ClientAddressSerializer
    queryset = ClientAddress.objects.all()
    permission_classes = [IsAuthenticated]

    def get_paginated_response(self, data):
        return Response(data)

    def get_queryset(self):
        return ClientAddress.objects.filter(client__user_id=self.request.user.pk).order_by('-is_default')

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))

        address = ClientAddress.objects.create(
            client=Client.objects.get(user_id=self.request.user.pk),
            address_name=data['addressName'],
            name=data['name'],
            surname=data['surname'],
            address=data['address'],
            zip_code=data['zipCode'],
            city=data['city'],
            comment=data.get('comment'),
            # latitude=data['latitude'], # TODO parsowanie do współrzędnych
            # longitude=data['longitude'],
            is_default=False,
            phone_number=data['phoneNumber']
        )
        serializer = ClientAddressSerializer(address)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))

        if len(data) > 2:
            ClientAddress.objects.filter(pk=data['id']).update(
                address_name=data.get('addressName'),
                name=data.get('name'),
                surname=data.get('surname'),
                address=data.get('address'),
                zip_code=data.get('zipCode'),
                city=data.get('city'),
                comment=data.get('comment'),
                # latitude=data['latitude'], # TODO parsowanie do współrzędnych
                # longitude=data['longitude'],
                phone_number=data.get('phoneNumber')
            )
        else:
            client_addresses = ClientAddress.objects.filter(client__user_id=self.request.user.pk)
            for address_data in client_addresses:
                address_data.is_default = False
                address_data.save()
            address = ClientAddress.objects.get(pk=data['id'])
            address.is_default = data.get('isDefault')
            address.save()

        address = ClientAddress.objects.get(pk=data['id'])

        serializer = ClientAddressSerializer(address)

        return Response(serializer.data)


class InvoiceData(viewsets.ModelViewSet):
    serializer_class = ClientInvoiceDataSerializer
    queryset = ClientInvoiceData.objects.all()
    permission_classes = [IsAuthenticated]

    def get_paginated_response(self, data):
        return Response(data)

    def get_queryset(self):
        return ClientInvoiceData.objects.filter(client__user_id=self.request.user.pk).order_by('-is_default')

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))

        invoice_data = ClientInvoiceData.objects.create(
            client=Client.objects.get(user_id=self.request.user.pk),
            name=data.get('name', ''),
            address=data['address'],
            zip_code=data['zipCode'],
            city=data['city'],
            nip=data['nip'],
            company_name=data['companyName'],
            is_default=False
        )
        serializer = ClientInvoiceDataSerializer(invoice_data)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))

        if len(data) > 2:
            ClientInvoiceData.objects.filter(pk=data['id']).update(
                name=data.get('name'),
                address=data.get('address'),
                zip_code=data.get('zipCode'),
                city=data.get('city'),
                nip=data.get('nip'),
                company_name=data.get('companyName'),
            )
        else:
            client_invoices_data = ClientInvoiceData.objects.filter(client__user_id=self.request.user.pk)
            for invoice in client_invoices_data:
                invoice.is_default = False
                invoice.save()
            invoice_data = ClientInvoiceData.objects.get(pk=data['id'])
            invoice_data.is_default = data.get('isDefault')
            invoice_data.save()

        invoice_data = ClientInvoiceData.objects.get(pk=data['id'])

        serializer = ClientInvoiceDataSerializer(invoice_data)

        return Response(serializer.data)


class PlacesView(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()
    permission_classes = [AllowAny]


class ClientView(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Client.objects.filter(user_id=self.request.user.pk)


class CategoriesForPlaceView(viewsets.ModelViewSet):
    serializer_class = CategoryInPlaceSerializer
    queryset = CategoryInPlace.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        place_id = self.kwargs['place_id']
        return CategoryInPlace.objects.filter(place_id=place_id, category__is_enabled=True)


class CategoriesView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_enabled=True)
    permission_classes = [AllowAny]


class ProductsInPlaceView(viewsets.ModelViewSet):
    serializer_class = ProductInPlaceSerializer
    queryset = ProductInPlace.objects.all()
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        place_id = self.kwargs['place_id']
        search_query = self.request.GET.get('search')
        queryset = ProductInPlace.objects.filter(place_id=place_id). \
            prefetch_related('product__product_set'). \
            prefetch_related('variant__product__productvariant_set'). \
            prefetch_related('variant__variant__productvariant_set'). \
            prefetch_related('product__productimage_set'). \
            prefetch_related('product__productdescriptionsection_set')

        if search_query:
            return queryset.filter(Q(product__name__icontains=search_query))
        else:
            return queryset


class ProductsInPlaceByCatView(viewsets.ModelViewSet):
    serializer_class = ProductInPlaceSerializer
    queryset = ProductInPlace.objects.all()
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        place_id = self.kwargs['place_id']
        category_id = self.kwargs['category_id']
        return ProductInPlace.objects.filter(place_id=place_id, product__category_id=category_id). \
            prefetch_related('product__product_set'). \
            prefetch_related('variant__product__productvariant_set'). \
            prefetch_related('variant__variant__productvariant_set'). \
            prefetch_related('product__productimage_set'). \
            prefetch_related('product__productdescriptionsection_set')


class ProductDetails(viewsets.ModelViewSet):
    serializer_class = ProductInPlaceSerializer
    queryset = ProductInPlace.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        place_id = self.kwargs['place_id']
        product_id = self.kwargs['product_id']
        return ProductInPlace.objects.filter(place_id=place_id, product_id=product_id)


class ProductImagesView(viewsets.ModelViewSet):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductImage.objects.filter(product_id=product_id)


class AddToCartView(viewsets.ModelViewSet):
    serializer_class = CartProductVariantSerializer
    queryset = CardProductVariant.objects.all()
    permission_classes = [IsAuthenticated]

    # adding product to cart
    @atomic
    def create(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        cart, _ = ClientCart.objects.get_or_create(
            client=Client.objects.get(user_id=self.request.user),
            is_closed=False
        )
        cart.last_update_date = datetime.datetime.now()
        cart.save()

        if not CardProductVariant.objects.filter(
                variant=ProductInPlace.objects.get(product_id=data.get('productId'),
                                                   variant=ProductVariant.objects.get(pk=data.get('variant')),
                                                   place_id=self.kwargs['place_id']),
                selected_variant=data['variant'],
                variant__place_id=self.kwargs['place_id'],
                cart_product__cart=cart
        ).exists():
            cart_product = CartProduct.objects.create(
                cart=cart,
                promo=data.get('promo', 0)
            )
        else:
            cart_product = CartProduct.objects.filter(
                cardproductvariant__variant=ProductInPlace.objects.get(product_id=data.get('productId'),
                                                                       variant=ProductVariant.objects.get(
                                                                           pk=data.get('variant')),
                                                                       place_id=self.kwargs['place_id']),
                cardproductvariant__variant__place_id=self.kwargs['place_id'],
                cardproductvariant__selected_variant=data['variant']
            ).first()

        product_variant, created = CardProductVariant.objects.get_or_create(
            cart_product=cart_product,
            variant=ProductInPlace.objects.get(product_id=data.get('productId'),
                                               variant=ProductVariant.objects.get(pk=data.get('variant')),
                                               place_id=self.kwargs['place_id']),
            selected_variant=data['variant'],
        )
        if not created:
            product_variant.quantity += float(data['quantity'])
        else:
            product_variant.quantity = float(data['quantity'])
        product_variant.save()

        serializer = CartProductVariantSerializer(product_variant)

        return Response(serializer.data)


class RemoveProductFromCartView(viewsets.ModelViewSet):
    serializer_class = CartProductVariantSerializer
    queryset = CardProductVariant.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        product_id = self.kwargs['product_id']
        cart_id = self.kwargs['cart_id']
        CardProductVariant.objects.get(pk=product_id, cart_product__cart_id=cart_id).delete()

        return Response(status=200)


class RemovePlaceFromCartView(viewsets.ModelViewSet):
    serializer_class = CartProductVariantSerializer
    queryset = CardProductVariant.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        place_id = self.kwargs['place_id']
        cart_id = self.kwargs['cart_id']
        CardProductVariant.objects.filter(variant__place_id=place_id, cart_product__cart_id=cart_id).delete()

        return Response(status=200)


class OpenClientCarts(viewsets.ModelViewSet):
    serializer_class = ClientCartSerializer
    queryset = ClientCart.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        carts = ClientCart.objects.filter(is_closed=False, client__user_id=self.request.user.pk)
        if not carts.exists():
            client = Client.objects.get(user_id=self.request.user.pk)
            ClientCart.objects.create(client=client, is_closed=False)
            carts = ClientCart.objects.filter(is_closed=False, client__user_id=self.request.user.pk)
        return carts


class ClientCartProducts(viewsets.ModelViewSet):
    serializer_class = CartProductVariantSerializer
    queryset = CardProductVariant.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        return CardProductVariant.objects.filter(cart_product__cart_id=cart_id)


class ClientDataView(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        data = json.loads((request.body.decode('utf-8')))

        user = User.objects.get(pk=self.request.user.pk)
        user.first_name = data.get('firstName')
        user.last_name = data.get('lastName')
        user.save()

        return Response(status=200)


class RemoveAddress(viewsets.ModelViewSet):
    serializer_class = ClientAddressSerializer
    queryset = ClientAddress.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        address_id = self.kwargs['address_id']
        ClientAddress.objects.get(pk=address_id).delete()

        return Response(status=200)


class RemoveInvoiceData(viewsets.ModelViewSet):
    serializer_class = ClientInvoiceDataSerializer
    queryset = ClientInvoiceData.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        invoice_data_id = self.kwargs['invoice_id']
        ClientInvoiceData.objects.get(pk=invoice_data_id).delete()

        return Response(status=200)


class CloseCartView(viewsets.ModelViewSet):
    serializer_class = ClientCartSerializer
    queryset = ClientCart.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        cart_id = self.kwargs['cart_id']
        cart = ClientCart.objects.get(pk=cart_id)
        cart.is_closed = True
        cart.save()

        return Response(status=200)


class ProductDescriptionSectionView(viewsets.ModelViewSet):
    serializer_class = ProductDescriptionSectionSerializer
    queryset = ProductDescriptionSection.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductDescriptionSection.objects.filter(product_id=product_id)


class UpdateCartProductQuantities(viewsets.ModelViewSet):
    serializer_class = CartProductVariantSerializer
    queryset = CardProductVariant.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        for product in data['data']:
            cart_product = CardProductVariant.objects.get(pk=product['id'])
            cart_product.quantity = product['quantity']
            cart_product.save()

        cart_id = self.kwargs['cart_id']
        cart = ClientCart.objects.get(pk=cart_id)
        cart.is_closed = True
        cart.save()

        return Response(status=200)


class CreateOrder(viewsets.ModelViewSet):
    serializer_class = OrderDetailsSerializer
    queryset = OrderDetails.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))['data']

        today_order_count = len(OrderDetails.objects.filter(create_date__contains=datetime.datetime.now().date()))
        delivery_date = datetime.datetime.fromisoformat(data.get('deliveryDate')) if data.get('deliveryDate') else None

        order = OrderDetails.objects.create(
            delivery_type=DeliveryType.objects.get(name=data.get('deliveryType')),
            client=Client.objects.get(user_id=self.request.user.pk),
            payment_method=PaymentType.objects.get(name=data.get('paymentMethod')),
            payment_status=4 if data['paymentMethod'] == 'collect' else 0,
            is_repeated=data.get('isRepeated'),
            order_price=data.get('orderPrice'),
            notes_for_order=data.get('notesForOrder'),
            order_id=f'#{today_order_count + 1}/{datetime.datetime.now().strftime("%d")}/{datetime.datetime.now().strftime("%m")}/{datetime.datetime.now().strftime("%Y")}',
            delivery_date=delivery_date
        )
        if data['selectedAddress'] != 0:
            order.delivery_address_id = data.get('selectedAddress')
            order.save()

        for product in data['products']:
            order.products.add(CardProductVariant.objects.get(pk=product['id']))

        if data['isRepeated']:
            repeatability = OrderRepeatability.objects.create(
                order=order,
                frequency=data.get('repeatFrequency')
            )
            for day in data['daysToRepeat']:
                repeatability.repeated_days.add(RepeatedDays.objects.get(day_number=day))

        message_collect = ''
        if order.status == 4:
            message_collect = 'Powiadomimy Cię, gdy Twoje zamówienie będzie gotowe do odbioru.'

        create_notification(self.request.user,
                            f'Potwierdzenie utworzenia zamówienia',
                            f"""Utworzono zamówienie o nr {order.order_id}. Zamówienie otrzymało status:
                            {order.get_status_display()}. {message_collect} """)

        return Response(status=200)


class ClientOrdersHistory(viewsets.ModelViewSet):
    serializer_class = OrderDetailsSerializer
    queryset = OrderDetails.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderDetails.objects.filter(products__cart_product__cart__is_closed=True,
                                           client__user=self.request.user).distinct().order_by('-id')


class GetClientRepeatedOrders(viewsets.ModelViewSet):
    serializer_class = OrderRepeatabilitySerializer
    queryset = OrderRepeatability.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        orders = OrderDetails.objects.filter(products__cart_product__cart__is_closed=True,
                                             client__user=self.request.user, is_repeated=True).distinct().order_by(
            '-id').values_list('pk', flat=True)
        repeatabilities = OrderRepeatability.objects.filter(order_id__in=orders)

        return repeatabilities


class GetOrderDetails(viewsets.ModelViewSet):
    serializer_class = OrderDetailsSerializer
    queryset = OrderDetails.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return OrderDetails.objects.filter(pk=order_id)


class GetOrderInvoice(viewsets.ModelViewSet):
    serializer_class = OrderInvoiceSerializer
    queryset = OrderInvoice.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return OrderInvoice.objects.filter(orders__in=[order_id])


class GetOrderRepeatability(viewsets.ModelViewSet):
    serializer_class = OrderRepeatabilitySerializer
    queryset = OrderRepeatability.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return OrderRepeatability.objects.filter(order_id=order_id)


class IssuesList(viewsets.ModelViewSet):
    serializer_class = OrderIssueSerializer
    queryset = OrderIssue.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return OrderIssue.objects.filter(order_id=order_id).order_by('-id')


class GetIssue(viewsets.ModelViewSet):
    serializer_class = OrderIssueSerializer
    queryset = OrderIssue.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        return Response(OrderIssueSerializer(OrderIssue.objects.filter(order_id=order_id).last()).data)


class ReportIssue(viewsets.ModelViewSet):
    serializer_class = OrderIssueSerializer
    queryset = OrderIssue.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        if request.headers['Content-Type'] == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
            issue = OrderIssue.objects.create(
                order_id=order_id,
                issue_type=data.get('issueType', 1),
                custom_issue_type=data.get('customIssueType', ''),
                description=data.get('description', ''),
                status=0
            )

        return Response(status=200)


class UploadIssueImage(viewsets.ModelViewSet):
    serializer_class = OrderIssueSerializer
    queryset = OrderIssue.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        issue = OrderIssue.objects.filter(order_id=order_id).last()

        if 'multipart/form-data' in request.headers['Content-Type']:
            if request.FILES:
                for i in request.FILES.getlist('image'):
                    issue_image = IssueImage.objects.create(
                        image=i
                    )
                    issue.issue_images.add(issue_image)
                    issue.save()

        return Response(status=200)


class RateProduct(viewsets.ModelViewSet):
    serializer_class = ProductRateSerializer
    queryset = ProductRate.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        user_id = self.request.user.pk
        product_id = self.kwargs['product_id']

        ProductRate.objects.create(
            product_id=product_id,
            user_id=user_id,
            rate=data.get('rate'),
            comment=data.get('comment')
        )

        return Response(status=200)


class GetInvoices(viewsets.ModelViewSet):
    serializer_class = OrderInvoiceSerializer
    queryset = OrderInvoice.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderInvoice.objects.prefetch_related('orders__products').filter(
            orders__client__user_id=self.request.user.pk).distinct('id')


class GetInvoiceData(viewsets.ModelViewSet):
    serializer_class = OrderInvoiceSerializer
    queryset = OrderInvoice.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        invoice_id = self.kwargs['invoice_id']

        return OrderInvoice.objects.filter(pk=invoice_id)


class OrderInvoiceForOrder(viewsets.ModelViewSet):
    serializer_class = OrderInvoiceSerializer
    queryset = OrderInvoice.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        selected_orders = []

        order_invoice = OrderInvoice.objects.create(
            status=0
        )
        for order in data.get('selectedOrders'):
            order_data = OrderDetails.objects.get(pk=order)
            order_invoice.orders.add(order_data)
            selected_orders.append(f'{order_data.order_id}')

        order_invoice.save()
        create_notification(self.request.user,
                            f'Zlecenie wystawienie faktury',
                            f'Zlecono wystawienie faktury do zamówień o nr: {", ".join(selected_orders)}')

        return Response(status=200)


class GetOrdersWithoutInvoice(viewsets.ModelViewSet):
    serializer_class = OrderDetailsSerializer
    queryset = OrderDetails.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderDetails.objects.filter(has_invoice=False, client__user_id=self.request.user.pk)


class TurnOffRepeat(viewsets.ModelViewSet):
    serializer_class = OrderDetailsSerializer
    queryset = OrderDetails.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        order = OrderDetails.objects.get(pk=order_id)
        order.is_repeated = False
        order.save()

        OrderRepeatability.objects.get(order_id=order_id).delete()

        return Response(status=200)


class GetIssueDetails(viewsets.ModelViewSet):
    serializer_class = OrderIssueConversationSerializer
    queryset = OrderIssueConversation.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        issue_id = self.kwargs['issue_id']

        issue, created = OrderIssueConversation.objects.get_or_create(
            issue_id=issue_id
        )

        return OrderIssueConversation.objects.filter(pk=issue.pk)


class IssueMessage(viewsets.ModelViewSet):
    serializer_class = OrderIssueMessageSerializer
    queryset = OrderIssueMessage.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        issue_id = self.kwargs['issue_id']
        try:
            data = json.loads(request.body.decode('utf-8'))
        except:
            data = request.POST

        message = OrderIssueMessage.objects.create(
            message=data.get('message', ''),
            author=data.get('author')
        )

        if request.FILES:
            message.image = request.FILES.get('image')
            message.save()

        issue = OrderIssueConversation.objects.get(issue_id=issue_id)
        issue.messages.add(message)
        issue.save()

        return Response(status=200)


class CopyProductsToCart(viewsets.ModelViewSet):
    serializer_class = OrderDetailsSerializer
    queryset = OrderDetails.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        cart = ClientCart.objects.create(
            client=Client.objects.get(pk=data['orderDetails']['client']['id']),
            is_closed=False
        )
        cart.last_update_date = datetime.datetime.now()
        cart.save()

        products_quantity = 0

        for product in data['orderDetails']['products']:
            cart_product = CartProduct.objects.create(
                cart=cart
            )

            product_variant = CardProductVariant.objects.create(
                cart_product=cart_product,
                variant=ProductInPlace.objects.get(product_id=product['selectedProductVariant']['product']['id'],
                                                   place_id=product['place']),
                selected_variant=product['selectedVariant'],
                quantity=product['quantity']
            )

            products_quantity += product['quantity']

        return JsonResponse({
            'productsQuantity': products_quantity,
            'cartId': cart.pk
        })


class UpdateRepeatability(viewsets.ModelViewSet):
    serializer_class = OrderDetailsSerializer
    queryset = OrderDetails.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        data = json.loads(request.body.decode('utf-8'))

        repeatability = OrderRepeatability.objects.get(order_id=order_id)
        repeatability.repeated_days.through.objects.filter(orderrepeatability_id=repeatability.pk).delete()
        for day in data.get('repeatDays'):
            repeatability.repeated_days.add(RepeatedDays.objects.get(day_number=day))
        repeatability.frequency = data.get('repeatFrequency')
        repeatability.save()

        return Response(status=200)


class AvailableDeliveryTypes(viewsets.ModelViewSet):
    serializer_class = DeliveryTypeSerializer
    queryset = DeliveryType.objects.all()
    permission_classes = [IsAuthenticated]


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-create_date')
