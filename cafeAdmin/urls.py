from django.urls import path
from .views import CategoriesView


urlpatterns = [
    path("", CategoriesView, name="index")
]