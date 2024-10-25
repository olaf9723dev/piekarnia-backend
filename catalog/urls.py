from django.urls import path

from .views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, ProductListView, \
    VariantsListView, VariantCreateView, VariantUpdateView, VariantDeleteView, VariantGroupListView, \
    VariantGroupCreateView, VariantGroupUpdateView, VariantGroupDeleteView, ProductListView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView, ProductInPlaceCreateView, ProductInPlaceUpdateView, ProductInPlaceDeleteView, \
    ProductImageDeleteView, ProductImageUpdateView, ProductImageCreateView, create_product_variant

urlpatterns = [
    path('variant_group_list', VariantGroupListView.as_view(), name='list_of_variant_group'),
    path('list/create_variant_group', VariantGroupCreateView.as_view(), name='variant_group_create'),
    path('list/<int:pk>/update_variant_group', VariantGroupUpdateView.as_view(), name='variant_group_update'),
    path('list/<int:pk>/delete_variant_group', VariantGroupDeleteView.as_view(), name='variant_group_delete'),
    path('variants_list', VariantsListView.as_view(), name='list_of_variants'),
    path('list/create_variant', VariantCreateView.as_view(), name='variant_create'),
    path('list/<int:pk>/update_variant', VariantUpdateView.as_view(), name='variant_update'),
    path('list/<int:pk>/delete_variant', VariantDeleteView.as_view(), name='variant_delete'),
    path('list_of_categories', CategoryListView.as_view(), name='list_of_categories'),
    path('list/create_category', CategoryCreateView.as_view(), name='category_create'),
    path('list/<int:pk>/update', CategoryUpdateView.as_view(), name='category_update'),
    path('list/<int:pk>/delete', CategoryDeleteView.as_view(), name='category_delete'),
    path('products_list', ProductListView.as_view(), name='list_of_products'),
    path('list/create_product', ProductCreateView.as_view(), name='product_create'),
    path('list/<int:pk>/update_product', ProductUpdateView.as_view(), name='product_update'),
    path('list/<int:pk>/delete_product', ProductDeleteView.as_view(), name='product_delete'),
    path('list/<int:place_id>/details/product-in-place/create/', ProductInPlaceCreateView.as_view(), name='product_in_place_create'),
    path('list/<int:place_id>/details/product-in-place/<int:product_id>/update/', ProductInPlaceUpdateView.as_view(), name='product_in_place_update'),
    path('list/<int:place_id>/details/product-in-place/<int:product_id>/delete/', ProductInPlaceDeleteView.as_view(), name='product_in_place_delete'),
    path('list/<int:pk>/update-product/images/create/', ProductImageCreateView.as_view(), name='product_image_create'),
    path('list/<int:pk>/update-product/images/<int:image_id>/update/', ProductImageUpdateView.as_view(), name='product_image_update'),
    path('list/<int:pk>/update-product/images/<int:image_id>/delete/', ProductImageDeleteView.as_view(), name='product_image_delete'),
    path('list/<int:pk>/update_product/variants/create', create_product_variant, name='create_product_variant'),
]
