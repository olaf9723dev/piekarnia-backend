import pprint

from django.conf import settings
from django.shortcuts import redirect
from django.templatetags.static import static
from rest_framework import viewsets

from catalog.models import Category, Product, ProductVariant, Variant, VariantGroup, ProductImage, ProductInPlace, \
    CategoryInPlace
from dotykackaApi.service import DotykackaApiService
from places.models import Place


class SyncDatabaseViewSet(viewsets.ViewSet):
    permission_classes = []

    def get(self, request):
        place_id = self.request.GET.get('place_id')
        place = Place.objects.get(pk=place_id)

        dotykacka_service = DotykackaApiService(place.refresh_token, place.cloud_id, settings.DOTYKACKA_GET_ACCESS_TOKEN_URL)
        dotykacka_service.authenticate()

        for category in dotykacka_service.get_categories(100)['data']:
            cat, created = Category.objects.get_or_create(
                name=category['name'],
                dotykacka_id=category['id']
            )
            cat_in_place, created2 = CategoryInPlace.objects.get_or_create(
                category=cat,
                place_id=place_id
            )

        product_pages = int(dotykacka_service.get_products(1, 100)['lastPage']) + 1
        for page_num in range(1, product_pages):
            for product_data in dotykacka_service.get_products(page_num, 100)['data']:
                # try:
                product, created = Product.objects.get_or_create(
                    category_id=Category.objects.get(dotykacka_id=product_data['_categoryId']).pk,
                    dotykacka_id=product_data['id']
                )
                product.net_price = round(float(product_data['priceWithoutVat']), 2)
                product.vat_base = float(product_data['vat'])
                product.name = product_data['name'].strip()
                product.is_promo = product_data['onSale']
                # product.product_code = product_data['plu'][0]
                if not product.description:
                    product.description = product_data['description']
                product.save()

                product_variant, created_v = ProductVariant.objects.get_or_create(
                    product=product,
                    extra_price=0,
                    unit=1 if product_data['unit'] == 'Kilogram' else 0,
                )
                if created_v:
                    variant_group, created_vg = VariantGroup.objects.get_or_create(
                        name='basic',
                        group_type=0
                    )
                    variant, created_var = Variant.objects.get_or_create(
                        name='basic',
                        group=variant_group
                    )
                    product_variant.variant.add(variant)

                product_image, created_img = ProductImage.objects.get_or_create(
                    product=product,
                    is_primary=True
                )

                product_in_place, created_pip = ProductInPlace.objects.get_or_create(
                    product=product,
                    place=place
                )
                if created_pip:
                    product_in_place.variant.add(product_variant)
                # except:
                #     pass

        return redirect('list_of_products')
