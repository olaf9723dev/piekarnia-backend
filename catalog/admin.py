from django.contrib import admin

from .models import Category, VariantGroup, Variant, Product, ProductVariant, ProductImage, ProductDescriptionSection, \
    ProductStatistic, ProductRate


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'is_enabled', 'parent')


@admin.register(VariantGroup)
class VariantGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_type', 'max_selected_count', 'min_selected_count')


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('name',
#     'group',
    'extra_price')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'net_price', 'vat_base', 'gross_price', 'short_description', 'description',
                    'is_promo', 'is_new', 'is_enabled')

#  TODO:
#   Fields ManyToMany:
#   'similar_products'
#   'tags'
#   'available_delivery_types'


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'extra_price', 'use_custom_stock', 'stock', 'unit',
                    'delivery_time', 'image', 'weight', 'is_enabled', 'get_variants')

    def get_variants(self, instance):
        return [instance for instance in instance.variant.all()]



@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'is_primary', 'order')


@admin.register(ProductDescriptionSection)
class ProductDescriptionSectionAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'content')


@admin.register(ProductStatistic)
class ProductStatisticAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'date')


@admin.register(ProductRate)
class ProductRateAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rate', 'date')
