from django.shortcuts import render, get_object_or_404
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


# def add_to_cart(request, slug):
#     item = get_object_or_404()






