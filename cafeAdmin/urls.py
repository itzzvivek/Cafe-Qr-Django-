from django.urls import path
from .views import register_cafe, welcome, manage_orders, order_detail, show_qr_code, login_view, manage_menu

app_name = "cafeAdmin"

urlpatterns = [
    path("register-cafe/", register_cafe, name="register-cafe"),
    path("login/", login_view, name='login'),
    path("welcome/", welcome, name="welcome"),
    path("manage-orders/", manage_orders, name="manage-orders"),
    path("order-detail/<int:order_id>/", order_detail, name="order-detail"),
    path("show-qr-code/<int:cafe_id>/", show_qr_code, name="show-qr-code"),
    path("manage_menu/", manage_menu, name="manage-menu"),
]
