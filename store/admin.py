from django.contrib import admin
from .models import Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'dietary', 'price', 'stock', 'is_active')
    list_filter = ('category', 'dietary', 'is_active')
    search_fields = ('name', 'cuisine', 'ingredients')
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'unit_price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'fulfillment', 'preferred_window', 'status', 'total_amount', 'created_at')
    list_filter = ('fulfillment', 'status', 'created_at')
    search_fields = ('full_name', 'email', 'user__username')
    inlines = [OrderItemInline]
