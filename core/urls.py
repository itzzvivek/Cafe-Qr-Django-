from django.urls import path
from .views import MenuViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'menu', MenuViewSet, basename='menu')
urlpatterns = router.urls
