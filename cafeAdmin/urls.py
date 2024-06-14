from django.urls import path
from .views import (register_cafe, CafeMenuView)

app_name = "cafeAdmin"

urlpatterns = [
    path("", CafeMenuView.as_view(), name="index"),
    path("register-cafe/", register_cafe, name="register-cafe"),
]
