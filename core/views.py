from django.shortcuts import render
from cafeAdmin.models import Category, MenuItem
from cafeAdmin.serializers import CategorySerializer, MenuItemSerializer
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related('items').all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        categories = self.get_queryset()
        serializers = self.get_serializer(categories, many=True)
        menu_items = MenuItem.objects.all()
        menu_item_serializer = MenuItemSerializer(menu_items, many=True)
        return render(request, 'user_temp/user_menu.html', {'categories': serializers.data,
                                                            'menu_items': menu_item_serializer.data})

