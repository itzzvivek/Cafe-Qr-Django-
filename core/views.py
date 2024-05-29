from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Category, MenuItem, Order, OrderItem, Payment, Refund, Coupon
from django.views.generic import ListView, DetailView, View


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


class OrderSummaryView(View):
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                order = Order.objects.get(user=self.request.user, ordered=False)
                context = {
                    'object': order
                }
                return render(self.request, 'user_temp/order_summary.html', context)
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
                return render(self.request, 'user_temp/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have an active order')
            return redirect("/")


def add_to_cart(request, slug):
    item = get_object_or_404(MenuItem, slug=slug)
    is_half_portion = request.GET.get('portion') == 'half'
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
                return redirect("core:menu")
            else:
                order.items.add(order_item)
                messages.info(request, "This item was added to your cart.")
                return redirect("core:menu")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart. ")
            return redirect("core:menu")
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
    return redirect("core:menu")


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
            return redirect("core:order-summary")
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
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:order-summary")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:menu", slug=slug)


