from rest_framework import serializers

from authentication.serializers import UserSerializer
from catalog.models import Category, VariantGroup, Variant, ProductVariant, ProductImage, ProductDescriptionSection, \
    ProductStatistic, ProductRate, Product, ProductInPlace
from core.models import Tag, DeliveryType
from places.serializers import PlaceSerializer


class CategorySerializer(serializers.ModelSerializer):
    isEnabled = serializers.BooleanField(source='is_enabled')
    dotykackaId = serializers.CharField(source='dotykacka_id')

    class Meta:
        model = Category
        fields = ["id", "name", "image", "isEnabled", "parent", "dotykackaId"]

    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields['parent'] = CategorySerializer(many=True)
        return fields


class VariantGroupSerializer(serializers.ModelSerializer):
    groupType = serializers.IntegerField(source='group_type')
    maxSelectedCount = serializers.IntegerField(source='max_selected_count')
    minSelectedCount = serializers.IntegerField(source='min_selected_count')

    class Meta:
        model = VariantGroup
        fields = ["id", "name", "groupType", "maxSelectedCount", "minSelectedCount"]


class VariantSerializer(serializers.ModelSerializer):
    group = VariantGroupSerializer(read_only=True)
    extraPrice = serializers.FloatField(source='extra_price')

    class Meta:
        model = Variant
        fields = ["id", "name", "group", "extraPrice"]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ["id", "name"]


class DeliveryTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryType
        fields = ["id", "name", "price", "icon"]


class SimpleProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    netPrice = serializers.FloatField(source='net_price')
    vatBase = serializers.FloatField(source='vat_base')
    shortDescription = serializers.CharField(source='short_description')
    isPromo = serializers.BooleanField(source='is_promo')
    isNew = serializers.BooleanField(source='is_new')
    isEnabled = serializers.BooleanField(source='is_enabled')
    productCode = serializers.CharField(source='product_code')

    class Meta:
        model = Product
        fields = ["id", "name", "category", "netPrice", "vatBase", "shortDescription", "isPromo", "isNew",
                  "isEnabled", "productCode"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    netPrice = serializers.FloatField(source='net_price')
    vatBase = serializers.FloatField(source='vat_base')
    shortDescription = serializers.CharField(source='short_description')
    isPromo = serializers.BooleanField(source='is_promo')
    isNew = serializers.BooleanField(source='is_new')
    similarProducts = SimpleProductSerializer(source='similar_products', many=True)
    isEnabled = serializers.BooleanField(source='is_enabled')
    productCode = serializers.CharField(source='product_code')
    avgRate = serializers.FloatField(source='avg_rate')
    mainImage = serializers.ImageField(source='main_image')
    # tags = TagSerializer(many=True, source="tag_set")
    # availableDeliveryTypes = DeliveryTypesSerializer(many=True, source="deliverytype_set")
    fattyAcids = serializers.FloatField(source='fatty_acids')

    class Meta:
        model = Product
        fields = ["id", "name", "category", "netPrice", "vatBase", "shortDescription", "description", "isPromo", "isNew",
                  "similarProducts", "isEnabled", "productCode", 'avgRate', "mainImage", "nutrition", "fat", "fattyAcids",
                  "carbohydrates", "sugar", "protein", "fiber", "salt"
                  # "tags", "availableDeliveryTypes"
                  ]


class ProductVariantSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variant = VariantSerializer(read_only=True, many=True)
    image = serializers.ImageField(read_only=True)
    extraPrice = serializers.FloatField(source='extra_price')
    useCustomStock = serializers.BooleanField(source='use_custom_stock')
    deliveryTime = serializers.FloatField(source='delivery_time')
    isEnabled = serializers.BooleanField(source='is_enabled')
    unitName = serializers.CharField(source='unit_name')

    class Meta:
        model = ProductVariant
        fields = ["id", "product", "variant", "extraPrice", "useCustomStock",
                  "stock", "unit", "deliveryTime", "image", "weight", "isEnabled", "unitName"]


class ProductImageSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    image = serializers.ImageField(read_only=True)
    isPrimary = serializers.BooleanField(source='is_primary', read_only=True)

    class Meta:
        model = ProductImage
        fields = ["id", "product", "image", "isPrimary", "order"]


class ProductDescriptionSectionSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductDescriptionSection
        fields = ["id", "product", "name", "content"]


class ProductStatisticSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserSerializer()

    class Meta:
        model = ProductStatistic
        fields = ["id", "product", "user", "date"]


class ProductRateSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserSerializer()

    class Meta:
        model = ProductRate
        fields = ["id", "product", "user", "rate", "date", "comment"]


class ProductInPlaceSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variant = ProductVariantSerializer(many=True)
    place = PlaceSerializer(read_only=True)
    customPrice = serializers.FloatField(source='custom_price')

    class Meta:
        model = ProductInPlace
        fields = ["id", "product", "place", "customPrice", "variant", "price"]


class CategoryInPlaceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    place = PlaceSerializer(read_only=True)

    class Meta:
        model = ProductInPlace
        fields = ["id", "place", "category"]
