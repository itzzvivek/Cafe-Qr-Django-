from django.urls import path
from .views import categories_view

app_name = "cafeAdmin"

urlpatterns = [
    path("", categories_view, name="index")
]
