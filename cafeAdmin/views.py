from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.db import transaction

from .models import Cafe
from .utils import generate_qr_code
from core.models import Category, MenuItem
from .forms import CafeRegisterForm
from .serializers import CategorySerializer, MenuItemSerializer


@transaction.atomic()
def register_cafe(request):
    if request.method == 'POST':
        form = CafeRegisterForm(request.POST)
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
            cafe.qr_code = qr_code
            return render(request, 'cafeAdmin_temp/welcome.html',
                          {'form': form, 'qr_code': qr_code, 'cafe_id': cafe.id})
    else:
        form = CafeRegisterForm()
    return render(request, 'cafeAdmin_temp/register_cafe.html', {'form': form})


def welcome(request):
    if request.user.is_authenticated:
        cafe = get_object_or_404(Cafe, owner=request.user)
        context = {
            'user': request.user,
            'cafe_id': cafe.id
        }
        return render(request, 'cafeAdmin_temp/welcome.html', context)
    else:
        return redirect('accounts:login')


def manage_orders(request):
    return render(request, 'cafeAdmin_temp/order_list.html')


def edit_menu(request):
    return render(request, 'cafeAdmin_temp/edit_menu.html')


def show_qr_code(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    context = {'cafe': cafe}
    return render(request, 'cafeAdmin_temp/show_qr_code.html', context)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
