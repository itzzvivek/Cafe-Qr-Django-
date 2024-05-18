from django.urls import path
from .views import menu_view, add_to_cart, OrderSummaryView


urlpatterns = [
    path('menu/', menu_view, name='menu'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('order-summary', OrderSummaryView.as_view(), name="order-summary"),
]
