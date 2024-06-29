from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.db import transaction

from .models import Cafe
from .utils import generate_qr_code
from core.models import Category, MenuItem
from .forms import CafeRegisterForm, LoginForm


@transaction.atomic()
def register_cafe(request):
    if request.method == 'POST':
        form = CafeRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            cafe_name = form.cleaned_data['cafe_name']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username=email, cafe_name=cafe_name, email=email, password=password)
            cafe = form.save(commit=False)
            cafe.owner = user
            cafe.save()
            return render(request, 'cafeAdmin_temp/welcome.html',
                          {'form': form, 'cafe_id': cafe.id})
    else:
        form = CafeRegisterForm()
    return render(request, 'cafeAdmin_temp/register_cafe.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('cafeAdmin:welcome')
            else:
                form.add_error('email', 'Incorrect email or password')
    else:
        form = LoginForm()
    return render(request, 'cafeadmin_temp/cafe_login.html', {'form': form})


@login_required()
def welcome(request):
    if request.user.is_authenticated:
        cafe = get_object_or_404(Cafe, owner=request.user)
        context = {
            'user': request.user,
            'cafe_id': cafe.id,
            'cafe': cafe,
        }
        return render(request, 'cafeAdmin_temp/welcome.html', context)
    else:
        return redirect('accounts:login')


@login_required()
def manage_orders(request):
    return render(request, 'cafeAdmin_temp/order_list.html')


@login_required()
def edit_menu(request):
    return render(request, 'cafeAdmin_temp/edit_menu.html')


@login_required()
def show_qr_code(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    unique_link = request.build_absolute_uri(reverse('core:menu', args=[cafe.id]))
    cafe.unique_link = unique_link
    qr_code = generate_qr_code(unique_link)
    cafe.qr_code = qr_code
    cafe.save()
    context = {'cafe': cafe}
    return render(request, 'cafeAdmin_temp/show_qr_code.html', context)


@login_required
def edit_menu(request):
    cafe = get_object_or_404(Cafe, owner=request.user)
    categories = Category.objects.filter(cafe=cafe)
    menu_items = MenuItem.objects.filter(cafe=cafe)

    context = {
        'categories': categories,
        'menu_items': menu_items,
        'cafe': cafe,
    }
    return render(request, 'cafeAdmin_temp/edit_menu.html', context)


@login_required
def manage_category(request, category_id=None):
    cafe = get_object_or_404(Cafe, owner=request.user)
    if category_id:
        category = get_object_or_404(Category, id=category_id, cafe=cafe)
    else:
        category = None

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.cafe = cafe
            new_category.save()
            return redirect('cafeAdmin:edit-menu')
    else:
        form = CategoryForm(instance=category)

    context = {'form': form, 'is_update': category_id is not None}
    return render(request, 'cafeAdmin_temp/manage_category.html', context)


@login_required
def delete_category(request, category_id):
    cafe = get_object_or_404(Cafe, owner=request.user)
    category = get_object_or_404(Category, id=category_id, cafe=cafe)
    category.delete()
    return redirect('cafeAdmin:edit-menu')


@login_required
def manage_menu_item(request, menu_item_id=None):
    cafe = get_object_or_404(Cafe, owner=request.user)
    if menu_item_id:
        menu_item = get_object_or_404(MenuItem, id=menu_item_id, cafe=cafe)
    else:
        menu_item = None

    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            new_menu_item = form.save(commit=False)
            new_menu_item.cafe = cafe
            new_menu_item.save()
            return redirect('cafeAdmin:edit-menu')
    else:
        form = MenuItemForm(instance=menu_item)

    context = {'form': form, 'is_update': menu_item_id is not None}
    return render(request, 'cafeAdmin_temp/manage_menu_item.html', context)