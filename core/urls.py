from django.urls import path
from .views import menu_view, CartView, add_to_cart, remove_single_item_from_cart, remove_from_cart, order_details

app_name = 'core'

urlpatterns = [
    path('menu/', menu_view, name='menu'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
    path('order-details/', order_details, name='order-details'),
]
