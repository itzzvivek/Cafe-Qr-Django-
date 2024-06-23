from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.db import transaction

from .utils import generate_qr_code
from core.models import Category, MenuItem
from .forms import CafeForm
from .serializers import CategorySerializer, MenuItemSerializer


@transaction.atomic()
def register_cafe(request):
    if request.method == 'POST':
        form = CafeForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username=username, email=username, password=password)

            cafe = form.save(commit=False)
            cafe.owner = user
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


@login_required
def welcome(request):
    return render(request, 'cafeAdmin_temp/landing_page.html')


@login_required
def manage_orders(request):
    return render(request, 'cafeAdmin_temp/order_list.html')


@login_required
def edit_menu(request):
    return render(request, 'cafeAdmin_temp/edit_menu.html')


@login_required
def show_qr_code(request):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
