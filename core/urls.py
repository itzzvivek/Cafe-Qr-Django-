from django.urls import path
from .views import menu_view, add_to_cart, OrderSummaryView, remove_from_cart


urlpatterns = [
    path('menu/', menu_view, name='menu'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
]
