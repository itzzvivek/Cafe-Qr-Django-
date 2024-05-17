from django.contrib import admin
from .models import Category, MenuItem, OrderItem, Order, Coupon, Payment, Refund


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

    make_refund_accepted.short_description = 'Update orders to refund granted'


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'max_price', 'min_price', 'category']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer_name',
                    'ordered',
                    'refund_requested',
                    'refund_granted',
                    'payment',
                    'coupon'
                    ]
    list_display_links = ['customer_name',
                          'payment',
                          'coupon',
                          ]
    list_filter = ['ordered',
                   'refund_requested',
                   'refund_granted',
                   ]
    search_fields = ['customer_name',
                     'ref_code',
                     ]
    actions = [make_refund_accepted]


admin.site.register(MenuItem,MenuItemAdmin)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(Coupon)
