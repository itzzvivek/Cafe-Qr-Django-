from django.urls import path
from .views import (menu_view,
                    CartView,
                    add_to_cart,
                    remove_single_item_from_cart,
                    remove_from_cart,
                    OrderDetailsView,
                    PaymentMethodsView,
                    thankyou,
                    )

app_name = 'core'

urlpatterns = [
    path('menu/<int:cafe_id>', menu_view, name='menu'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-single-item-from-cart/<slug:slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('remove-from-cart/<slug:slug>/', remove_from_cart, name="remove-from-cart"),
    path('order-details/<int:order_id>', OrderDetailsView.as_view(), name='order-details'),
    path('payment-method/<int:order_id>/', PaymentMethodsView.as_view(), name='payment-method'),
    path('thank-you/<int:order_id>', thankyou, name='thank-you'),
]
