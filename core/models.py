from django.db import models
from django.shortcuts import reverse
from cafeAdmin.models import Cafe
from django.contrib.auth.models import User

PAYMENT_CHOICES = [
    ('cash', 'Cash'),
    ('razorpay', 'Razorpay')
]


class Category(models.Model):
    name = models.CharField(max_length=100)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu_images', blank=True)
    max_price = models.DecimalField(max_digits=5, decimal_places=2)
    min_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=False, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug,
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug,
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug,
        })

    def get_remove_single_item_from_cart_url(self):
        return reverse("core:remove-single-item-from-cart", kwargs={'slug': self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_half_portion = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_item_price(self):
        return self.item.min_price if self.is_half_portion else self.item.max_price

    def get_total_item_price(self):
        return self.quantity * self.get_item_price()

    def get_total_discount_item_price(self):
        if hasattr(self.item, 'discount_price'):
            return self.quantity * self.item.discount_price
        return self.get_total_item_price()

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        return self.get_total_discount_item_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.AutoField(primary_key=True, unique=True, editable=False)
    customer_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    table_number = models.IntegerField()
    message = models.TextField()
    items = models.ManyToManyField(OrderItem, related_name='orders')
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_name

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            if order_item.is_half_portion:
                total += order_item.item.min_price * order_item.quantity
            else:
                total += order_item.item.max_price * order_item.quantity
        return total


class Payment(models.Model):
    payment_charge_id = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=50)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)

    def __str__(self):
        return f"{self.customer_name} - {self.amount}"


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
