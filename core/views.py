import json
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Category, MenuItem, Order, OrderItem, Payment
from django.views.generic import View
from cafeAdmin.models import Cafe

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))


def menu_view(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    categories = Category.objects.filter(cafe=cafe)
    menu_items = []
    for category in categories:
        items = MenuItem.objects.filter(category=category, cafe=cafe)
        menu_items.append((category, items))
    context = {
        'categories': categories,
        'menu_items': menu_items,
        'cafe': cafe,
        'message': "Welcome to our cafe! Enjoy your meal."
    }
    return render(request, 'user_temp/user_menu.html', context)


class CartView(View):
    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        order_items = []
        total = 0
        for key, item in cart.items():
            try:
                menu_item = MenuItem.objects.get(slug=key.split("_")[0])
                total += float(item['price']) * item['quantity']
                order_items.append({
                    'item': menu_item,
                    'quantity': item['quantity'],
                    'total_price': float(item['price']) * item['quantity'],
                    'is_half_portion': item["is_half_portion"]
                })
            except MenuItem.DoesNotExist:
                continue
        context = {
            'order_items': order_items,
            'total': total
        }
        return render(request, 'user_temp/cart.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        table = request.POST.get('table')
        message = request.POST.get('message')

        if not all([name, phone, table]):
            messages.warning(request, 'Please fill all the fields')
            return redirect("core:cart")

        cart = request.session.get('cart', {})
        if not cart:
            messages.warning(request, "Your cart is empty")
            return redirect("core:cart")

        default_cafe = Cafe.objects.first()

        # Create a new order
        order = Order.objects.create(
            customer_name=name,
            phone_number=phone,
            table_number=table,
            message=message,
            ordered=False,
            ordered_date=timezone.now(),
            cafe=default_cafe
        )

        # Add items to the new order
        for key, item in cart.items():
            try:
                menu_item = MenuItem.objects.get(slug=key.split("_")[0])
                is_half_portion = item["is_half_portion"]
                quantity = item["quantity"]
                order_item = OrderItem.objects.create(
                    item=menu_item,
                    quantity=quantity,
                    is_half_portion=is_half_portion,
                    ordered=False,
                    order=order  # Associate this OrderItem with the new Order
                )
            except MenuItem.DoesNotExist:
                continue

        # Save the new order
        order.save()

        # Store order details in the session for later use
        request.session['order_details'] = {
            'name': name,
            'phone': phone,
            'table': table,
            'message': message,
        }

        # Clear the cart
        request.session['cart'] = {}

        messages.success(request, 'Order has been successfully created')
        return redirect("core:order-details", order_id=order.pk)


def add_to_cart(request, slug):
    item = get_object_or_404(MenuItem, slug=slug)
    is_half_portion = request.GET.get('portion') == 'half'
    quantity = int(request.GET.get('quantity', 1))

    if quantity <= 0:
        messages.warning(request, 'Quantity must be greater than zero')
        return redirect("core:menu")

    cart = request.session.get('cart', {})
    portion_key = 'half' if is_half_portion else 'full'
    cart_key = f"{slug}_{portion_key}"
    cart_item = cart.get(cart_key, {
        'name': item.name,
        'quantity': 0,
        'price': str(item.min_price if is_half_portion else item.max_price),
        'is_half_portion': is_half_portion
    })
    cart_item['quantity'] += quantity
    cart[cart_key] = cart_item
    request.session['cart'] = cart
    messages.info(request, "This item was added to your cart.")
    return redirect("core:cart")


def remove_from_cart(request, slug):
    cart = request.session.get('cart', {})
    portion_key = 'half' if request.GET.get('portion') == 'half' else 'full'
    cart_key = f"{slug}_{portion_key}"

    if cart_key in cart:
        del cart[cart_key]
        request.session['cart'] = cart
        messages.info(request, "This item was removed from your cart.")
    else:
        messages.info(request, "This item was not in your cart.")

    return redirect("core:cart")


def remove_single_item_from_cart(request, slug):
    cart = request.session.get('cart', {})
    portion_key = 'half' if request.GET.get('portion') == 'half' else 'full'
    cart_key = f"{slug}_{portion_key}"

    if cart_key in cart:
        cart_item = cart[cart_key]
        if cart_item['quantity'] > 1:
            cart_item['quantity'] -= 1
            cart[cart_key] = cart_item
            request.session['cart'] = cart
            messages.info(request, "This item quantity was updated.")
        else:
            del cart[cart_key]
            request.session['cart'] = cart
            messages.info(request, "This item was removed from your cart.")
    else:
        messages.info(request, "This item was not in your cart.")

    return redirect("core:cart")


class OrderDetailsView(View):
    def get(self, request, order_id, *args, **kwargs):
        order_details = request.session.get('order_details', {})
        order_items = []
        total = 0

        try:
            order = get_object_or_404(Order, pk=order_id)
            for order_item in order.order_items.all():
                order_items.append({
                    'item': order_item.item,
                    'quantity': order_item.quantity,
                    'price': order_item.get_item_price(),
                    'total_price': order_item.get_final_price(),
                    'is_half_portion': order_item.is_half_portion
                })
                total += order_item.get_final_price()
        except ObjectDoesNotExist:
            order = None

        context = {
            'order': order,
            'order_items': order_items,
            'total': total,
            'order_details': order_details,
            'order_id': order_id
        }
        return render(request, 'user_temp/order_details.html', context)


class PaymentMethodsView(View):
    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, pk=order_id, ordered=False)
        total = order.get_total()
        context = {
            'order_id': order_id,
            'total': total
        }
        return render(request, 'user_temp/payments.html', context)

    def post(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, pk=order_id, ordered=False)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        payment_method = body.get('payment_method')
        print(payment_method)
        customer_name = order.customer_name

        if payment_method == "cash":
            payment = Payment.objects.create(
                razorpay_charge_id='N/A',
                customer_name=order.customer_name,
                amount=order.get_total(),
                payment_method="cash"
            )
            order.payment = payment
            order.ordered = True
            order.save()
            if 'cart' in request.session:
                request.session['cart'] = {}
            return JsonResponse({"redirect_url": '/thank-you'})

        else:
            if 'razorpay_payment_id' in request.POST:
                # Handling the UPI payment response
                razorpay_payment_id = request.POST.get('razorpay_payment_id')
                razorpay_order_id = request.POST.get('razorpay_order_id')
                razorpay_signature = request.POST.get('razorpay_signature')

                # Verify the payment using Razorpay SDK
                params_dict = {
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature
                }

                try:
                    razorpay_client.utility.verify_payment_signature(params_dict)
                    payment = get_object_or_404(Payment, razorpay_charge_id=razorpay_order_id)
                    payment.razorpay_charge_id = razorpay_payment_id
                    payment.payment_method = 'razorpay'
                    payment.save()
                    order.payment = payment
                    order.ordered = True
                    order.save()
                    if 'cart' in request.session:
                        request.session['cart'] = {}
                    return JsonResponse({"redirect_url": '/thank-you'})
                except razorpay.errors.SignatureVerificationError:
                    return JsonResponse({"error": "Payment verification failed."}, status=400)
            else:
                # Create Razorpay order for UPI payment
                total_amount = order.get_total() * 100
                currency = "INR"

                razorpay_order = razorpay_client.order.create({
                    "amount": int(total_amount),
                    "currency": currency,
                    "payment_capture": "1"
                })

                payment = Payment.objects.create(
                    razorpay_charge_id=razorpay_order['id'],
                    customer_name=order.customer_name,
                    amount=order.get_total(),
                    payment_method='razorpay'
                )

                order.payment = payment
                order.save()

                context = {
                    "razorpay_order_id": razorpay_order['id'],
                    "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                    "amount": float(total_amount),
                    "name": request.user.username,
                    "email": request.user.email,
                    "customer_name": customer_name,
                }

                return JsonResponse(context)


def thankyou(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    context = {
        'order': order,
    }
    return render(request, 'user_temp/thank_you.html', {'context': context})


