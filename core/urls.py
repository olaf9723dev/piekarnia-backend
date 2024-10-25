from django.urls import path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from .views import Addresses, InvoiceData, PlacesView, ClientView, CategoriesForPlaceView, ProductsInPlaceView, \
    ProductImagesView, AddToCartView, ProductDetails, ClientCartProducts, OpenClientCarts, \
    RemoveProductFromCartView, RemovePlaceFromCartView, ClientDataView, RemoveInvoiceData, RemoveAddress, CloseCartView, \
    ProductDescriptionSectionView, UpdateCartProductQuantities, ClientOrdersHistory, CreateOrder, \
    GetOrderDetails, GetOrderInvoice, GetOrderRepeatability, ReportIssue, IssuesList, RateProduct, GetInvoices, \
    OrderInvoiceForOrder, GetInvoiceData, GetOrdersWithoutInvoice, TurnOffRepeat, GetIssueDetails, IssueMessage, \
    CategoriesView, CopyProductsToCart, UpdateRepeatability, UploadIssueImage, GetClientRepeatedOrders, \
    ProductsInPlaceByCatView, AvailableDeliveryTypes, NotificationViewSet

urlpatterns = [
    path('mobile-devices/', FCMDeviceAuthorizedViewSet.as_view({"post": "create"})),
    path('addresses/', Addresses.as_view({'get': 'list', 'post': 'create', 'put': 'update'}), name='addresses'),
    path('addresses/<int:pk>', Addresses.as_view({'delete': 'destroy'}), name='remove_address'),
    path('invoice-data/', InvoiceData.as_view({'get': 'list', 'post': 'create', 'put': 'update'}), name='invoice_data'),
    path('invoice-data/<int:pk>', InvoiceData.as_view({'delete': 'destroy'}), name='remove_invoice_data'),
    path('places/', PlacesView.as_view({'get': 'list'}), name='places'),
    path('client/', ClientView.as_view({'get': 'list'}), name='client'),
    path('client/change-data/', ClientDataView.as_view({'put': 'update'}), name='client_data'),
    path('categories/', CategoriesView.as_view({'get': 'list'}), name='categories'),
    path('categories/<int:place_id>/', CategoriesForPlaceView.as_view({'get': 'list'}), name='categories'),

    path('product-offer/<int:place_id>/', ProductsInPlaceView.as_view({'get': 'list'}), name='product_offer'),
    path('product-offer/<int:place_id>/category/<int:category_id>/', ProductsInPlaceByCatView.as_view({'get': 'list'}), name='product_offer_by_cat'),
    path('product-offer/<int:place_id>/product-description/<int:product_id>/',
         ProductDescriptionSectionView.as_view({'get': 'list'}), name='product_description'),
    path('product-offer/<int:place_id>/product-details/<int:product_id>/', ProductDetails.as_view({'get': 'list'}),
         name='product_details'),
    path('product-offer/<int:place_id>/product-details/<int:product_id>/images/',
         ProductImagesView.as_view({'get': 'list'}), name='product_images'),

    path('product-offer/<int:place_id>/product-details/<int:product_id>/add-cart/',
         AddToCartView.as_view({'post': 'create'}), name='add_to_cart'),
    path('product-offer/<int:cart_id>/<int:product_id>/remove-cart-product/',
         RemoveProductFromCartView.as_view({'delete': 'destroy'}), name='remove_product_from_cart'),
    path('product-offer/<int:cart_id>/<int:place_id>/remove-cart-place/',
         RemovePlaceFromCartView.as_view({'delete': 'destroy'}), name='remove_place_from_cart'),
    path('cart/', OpenClientCarts.as_view({'get': 'list'}), name='get_open_cart'),
    path('cart/<int:cart_id>/', ClientCartProducts.as_view({'get': 'list'}), name='get_cart_products'),
    path('cart/<int:cart_id>/close/', CloseCartView.as_view({'post': 'update'}), name='close_cart'),
    path('cart/<int:cart_id>/update-quantities/', UpdateCartProductQuantities.as_view({'post': 'update'}),
         name='update_cart'),

    path('create-order/', CreateOrder.as_view({'post': 'create'}), name='create_order'),
    path('order-history/', ClientOrdersHistory.as_view({'get': 'list'}), name='order_history'),
    path('order-history/<int:order_id>/order-details/', GetOrderDetails.as_view({'get': 'list'}), name='order_details'),
    path('order-history/<int:order_id>/order-details/order-invoice/', GetOrderInvoice.as_view({'get': 'list'}),
         name='order_invoice'),
    path('order-history/<int:order_id>/order-details/order-repeatability/',
         GetOrderRepeatability.as_view({'get': 'list'}), name='order_repeatability'),
    path('order-history/<int:order_id>/order-details/report-issue/', ReportIssue.as_view({'post': 'create'}),
         name='report_issue'),
    path('order-history/<int:order_id>/order-details/upload-images/', UploadIssueImage.as_view({'post': 'create'}),
         name='upload_issue_image'),
    path('order-history/<int:order_id>/order-details/issues/', IssuesList.as_view({'get': 'list'}),
         name='order_issues'),
    path('order-history/<int:order_id>/order-details/issues/<int:issue_id>/issue-details/',
         GetIssueDetails.as_view({'get': 'list'}),
         name='get_issue_details'),
    path('order-history/<int:order_id>/order-details/issues/<int:issue_id>/issue-details/send-message/',
         IssueMessage.as_view({'post': 'create'}), name='send_message'),
    path('order-history/<int:order_id>/order-details/turnoff-repeat/', TurnOffRepeat.as_view({'post': 'update'}),
         name='turnoff_update'),
    path('order-history/<int:order_id>/order-details/copy-to-cart/', CopyProductsToCart.as_view({'post': 'create'}), name='copy_to_cart'),
    path('order-history/<int:order_id>/order-details/update-repeatability/', UpdateRepeatability.as_view({'put': 'update'}), name='copy_to_cart'),

    path('rate_product/<int:product_id>/', RateProduct.as_view({'post': 'create'}), name='rate_product'),
    path('invoices/', GetInvoices.as_view({'get': 'list'}), name='get_invoices'),
    path('invoices/<int:invoice_id>/invoice-details/', GetInvoiceData.as_view({'get': 'list'}),
         name='get_invoice_data'),
    path('invoices/order-invoice/', OrderInvoiceForOrder.as_view({'post': 'create'}), name='order_invoice'),
    path('invoices/invoiceless-orders/', GetOrdersWithoutInvoice.as_view({'get': 'list'}), name='invoiceless_orders'),

    path('calendar/client-repeated-orders/', GetClientRepeatedOrders.as_view({'get': 'list'}), name='client_repeated_orders'),
    path('delivery-types/', AvailableDeliveryTypes.as_view({'get': 'list'}), name='available_delivery_types'),
    path('notifications/', NotificationViewSet.as_view({'get': 'list'}), name='notifications')
]
