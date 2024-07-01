from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib import messages

from .models import Cafe
from .utils import generate_qr_code
from core.models import Category, MenuItem
from .forms import CafeRegisterForm, LoginForm, CategoryForm, MenuItemForm


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
    return render(request, 'cafeAdmin_temp/manage_menu.html')


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
def manage_menu(request):
    cafe = get_object_or_404(Cafe, owner=request.user)

    category_form = CategoryForm(request.POST or None)

    menu_item_form = MenuItemForm(request.POST or None)

    if request.method == 'POST':
        if 'save_category' in request.POST and category_form.is_valid():
            category = category_form.save(commit=False)
            category.cafe = cafe
            category.save()
            messages.success(request, "Category saved successfully")
            return redirect('cafeAdmin:manage-menu')

        if 'save_menu_item' in request.POST and menu_item_form.is_valid():
            menu_item = menu_item_form.save(commit=False)
            menu_item.cafe = cafe
            menu_item.save()
            messages.success(request, "Menu item saved successfully.")
            return redirect('cafeAdmin:manage-menu')

        if 'delete_category' in request.POST:
            category_name = request.POST.get('delete_category')
            category = get_object_or_404(Category, name=category_name, cafe=cafe)
            category.delete()
            messages.success(request, "Category deleted successfully.")
            return redirect('cafeAdmin:manage-menu')

        if 'delete_menu_item' in request.POST:
            menu_item_name = request.POST.get('delete_menu_item')
            menu_item = get_object_or_404(MenuItem, name=menu_item_name, cafe=cafe)
            menu_item.delete()
            messages.success(request, 'Menu item deleted successfully.')
            return redirect('cafeAdmin:manage-menu')
    else:
        category_form = CategoryForm()
        menu_item_form = MenuItemForm()

    categories = Category.objects.filter(cafe=cafe)
    menu_items = MenuItem.objects.filter(cafe=cafe)

    context = {
        'categories': categories,
        'menu_items': menu_items,
        'category_form': category_form,
        'menu_item_form': menu_item_form,
        'cafe': cafe,
    }
    return render(request, 'cafeAdmin_temp/manage_menu.html', context)