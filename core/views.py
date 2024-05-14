from django.shortcuts import render
from cafeAdmin.models import Category, MenuItem


# def menu_view(request):
#     # category = request.GET.get('category')
#     # menu_items = MenuItem.objects.filter(category=category)
#     menu_items = MenuItem.objects.all()
#     categories = Category.objects.all()
#     context = {'categories': categories,
#                'menu_items': menu_items}
#     return render(request, 'user_temp/user_menu.html', context)


def menu_view(request):
    categories = Category.objects.all()
    menu_items = []
    for category in categories:
        items = MenuItem.objects.filter(category=category)
        menu_items.append((category, items))
    return render(request, 'user_temp/user_menu.html', {'categories': categories, 'menu_items': menu_items})







