from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category, MenuItem, Order, OrderItem, Payment, Refund, Coupon
from django.views.generic import ListView, DetailView, View
import json


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


class CartView(View):
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                order = Order.objects.get(user=self.request.user, ordered=False)
                context = {
                    'object': order
                }
                return render(self.request, 'user_temp/cart.html', context)
            else:
                cart = request.session.get('cart', {})
                order_items = []
                total = 0
                for key, item in cart.items():
                    total += float(item['price']) * item['quantity']
                    order_items.append({
                        'item': item,
                        'quantity': item['quantity'],
                        'total_price': float(item['price']) * item['quantity'],
                        'is_half_portion': item["is_half_portion"]
                    })
                context = {
                    'order_items': order_items,
                    'total': total
                }
                return render(self.request, 'user_temp/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have an active order')
            return redirect("/")


def add_to_cart(request, slug):
    item = get_object_or_404(MenuItem, slug=slug)
    is_half_portion = request.GET.get('portion') == 'half'
    quantity = int(request.GET.get('quantity', 1))

    if quantity <= 0:
        messages.warning(request, 'Quantity must be greater than zero')

    if request.user.is_authenticated:
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False,
            is_half_portion=is_half_portion
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug, is_half_portion=is_half_portion).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                return redirect("core:cart")
            else:
                order.items.add(order_item)
                messages.info(request, "This item was added to your cart.")
                return redirect("core:cart")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart. ")
            return redirect("core:cart")
    else:
        cart = request.session.get('cart', {})
        portion_key = 'half' if is_half_portion else 'full'
        cart_key = f"{slug}_{portion_key}"
        cart_item = cart.get(cart_key, {
            'name': item.name,
            'quantity': 0,
            'price': str(item.min_price if is_half_portion else item.max_price),
            'is_half_portion': is_half_portion
        })
        cart_item['quantity'] += 1
        cart[slug] = cart_item
        request.session['cart'] = cart
    messages.info(request, "This item was added to your cart.")
    return redirect("core:cart")


def remove_from_cart(request, slug):
    item = get_object_or_404(MenuItem, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:menu", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:menu", slug=slug)


def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(MenuItem, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:menu", slug=slug)


class OrderDetailsView(View):
    def get(self, request, *args, **kwargs):
        order_details = request.sesion.get('order_details', {})
        try:
            if request.user.is_authenticated:
                order = Order.objects.get(user=self.request.user, ordered=False)
                context = {
                    'object': order,
                    'order_details': order_details
                }
            else:
                cart = request.session.get('cart', {})
                order_items = []
                total = 0
                for key, item in cart.items():
                    total += float(item['price']) * item['quantity']
                    order_items.append({
                        'item': item,
                        'quantity': item['quantity'],
                        'total_price': float(item['price']) * float(item['quantity']),
                        'is_half_portion': item['is_half_portion']
                    })
                context = {
                    'order_items': order_items,
                    'total': total,
                    'order_details': order_details
                }
            return render(request, 'user_temp/order_details.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


@csrf_exempt
def update_order_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        status = data.get('status')
        try:
            order = Order.Objects.get(id=order_id)
            order.status = status
            order.save()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return jsonResponse({'success': False, 'error': 'Order not found'})
    return JsonResponse({'success': True, 'error': 'Invalid request method'})
