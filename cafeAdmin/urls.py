from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import register_cafe, CategoryViewSet, MenuItemViewSet

app_name = "cafeAdmin"

router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'menuitems', MenuItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("register-cafe/", register_cafe, name="register-cafe"),
]
