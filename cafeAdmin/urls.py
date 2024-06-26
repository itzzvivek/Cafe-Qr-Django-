from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import register_cafe, welcome, edit_menu, manage_orders, show_qr_code, CategoryViewSet, MenuItemViewSet

app_name = "cafeAdmin"

router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'menuitems', MenuItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("register-cafe/", register_cafe, name="register-cafe"),
    path("welcome/", welcome, name="welcome"),
    path("manage-orders/", manage_orders, name="manage-orders"),
    path("edit-menu/", edit_menu, name="edit-menu"),
    path("show-qr-code/<int:cafe_id>/", show_qr_code, name="show-qr-code"),
]
