from django.shortcuts import render
from cafeAdmin.models import Category, MenuItem


def menu_view(request):
    categories = Category.objects.all()
    menu_items = []
    for category in categories:
        items = MenuItem.objects.filter(category=category)
        menu_items.append((category, items))
    context = {
        'categories': categories,
        'menu_items': menu_items
    }
    return render(request, 'user_temp/user_menu.html', context)









