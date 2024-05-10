from django.contrib import admin
from .models import Category, MenuItem


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'max_price', 'min_price', 'category']


admin.site.register(MenuItem,MenuItemAdmin)
admin.site.register(Category)
