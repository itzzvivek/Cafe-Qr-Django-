from django.shortcuts import render
from cafeAdmin.models import Category, MenuItem


def menu_view(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    return render(request, 'user_temp/user_menu.html',
                  {'categories': categories, 'menu_items': menu_items})






