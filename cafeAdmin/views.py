from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .utils import generate_qr_code

from core.models import Category, MenuItem
from .forms import CafeForm
from .serializers import CategorySerializer, MenuItemSerializer


def register_cafe(request):
    if request.method == 'POST':
        form = CafeForm(request.POST)
        if form.is_valid():
            cafe = form.save(commit=False)
            cafe.owner = request.user
            cafe.save()
            unique_link = request.build_absolute_uri(reverse('core:menu', args=[cafe.id]))
            cafe.unique_link = unique_link
            cafe.save()
            qr_code = generate_qr_code(unique_link)
            return render(request, 'cafeAdmin_temp/register_cafe.html',
                          {'form': form, 'qr_code': qr_code})
    else:
        form = CafeForm()
    return render(request, 'cafeAdmin_temp/register_cafe.html', {'form': form})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
