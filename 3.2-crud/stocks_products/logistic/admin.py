from django.contrib import admin
from django.forms import BaseInlineFormSet

from .models import Product, Stock, StockProduct

class StockProductInline(admin.TabularInline):
    model = StockProduct
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    # list_filter = ['']

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'address']
    inlines = [StockProductInline, ]
    # list_filter = ['']
    