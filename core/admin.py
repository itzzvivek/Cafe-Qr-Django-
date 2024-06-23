from django.contrib import admin
from .models import Category, MenuItem, OrderItem, Order, Coupon, Payment, Refund
from cafeAdmin.models import Cafe


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

    make_refund_accepted.short_description = 'Update orders to refund granted'


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'name', 'max_price', 'min_price', 'category']
    list_filter = ['cafe', 'category']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'refund_requested',
                    'refund_granted',
                    'payment',
                    'coupon'
                    ]
    list_display_links = ['user',
                          'payment',
                          'coupon',
                          ]
    list_filter = ['ordered',
                   'refund_requested',
                   'refund_granted',
                   ]
    search_fields = ['user__username',
                     'ref_code',
                     ]
    actions = [make_refund_accepted]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'cafe']
    list_filter = ['cafe',]


admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(Coupon)
