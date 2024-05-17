from django.shortcuts import render, get_object_or_404
from cafeAdmin.models import Category, MenuItem, Order, OrderItem, Payment, Refund, Coupon


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


def add_to_cart(request, slug):
    item = get_object_or_404(MenuItem, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.object.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("user:order-summary")
        else:
            order.items.add(order_item)
            message.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        order_date = timezone.now()
        order = Order.object.create(
            user=request.user, ordered_data=ordered_date)
        order.items.add(order_item)
        message.info(request, "This item was added to your cart. ")
        return redirect("user:order-summary")






