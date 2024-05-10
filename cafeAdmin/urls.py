from django.urls import path
from .views import categories_view


urlpatterns = [
    path("", categories_view, name="index")
]
