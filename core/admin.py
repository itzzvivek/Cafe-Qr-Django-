from django.contrib import admin
from .models import Category, MenuItem, OrderItem, Order, Coupon, Payment, Refund


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'name', 'max_price', 'min_price', 'category']
    list_filter = ['cafe', 'category']


class OrderAdmin(admin.ModelAdmin):
    list_display = [
                    'user',
                    'customer_name',
                    'ordered_date',
                    'refund_requested',
                    'refund_granted',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
                          'payment',
                          'coupon',
                          ]
    list_filter = [
                    'cafe',
                    'ordered_date',
                    'refund_requested',
                    'refund_granted',
                   ]
    search_fields = [
                     'ref_code',
                     ]
    actions = [make_refund_accepted]

    inlines = [OrderItemInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'cafe']
    list_filter = ['cafe',]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'is_half_portion', 'order')


admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(Coupon)
