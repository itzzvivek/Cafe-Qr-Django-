from django.urls import path
from .views import (menu_view,
                    CartView,
                    add_to_cart,
                    remove_single_item_from_cart,
                    remove_from_cart,
                    OrderDetailsView,
                    update_order_status,
                    PaymentMethodsView,
                    thankyou
                    )

app_name = 'core'

urlpatterns = [
    path('menu/<int:cafe_id>', menu_view, name='menu'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
    path('order-details/<int:pk>', OrderDetailsView.as_view(), name='order-details'),
    path('update-order-status/', update_order_status, name='update-order-status'),
    path('payment-method/<int:order_id>/', PaymentMethodsView.as_view(), name='payment-method'),
    path('thank-you/<int:order_id>', thankyou, name='thank-you')
]
