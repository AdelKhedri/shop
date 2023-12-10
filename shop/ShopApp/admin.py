from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Product, Shop, Social, BuyProduct
# Register your models here.

class ShopRegister(admin.ModelAdmin):
    list_display = ('name', 'username', 'manager', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('name', 'username', 'manager', 'is_active',)

class CategoryRegister(admin.ModelAdmin):
    list_display = ('name', 'shop', 'for_sell',)

class ProductRegister(admin.ModelAdmin):
    list_display = ('name', 'price', 'shop',)
    list_filter = ('shop',)
    search_fields = ('name', 'shop', 'description',)

class SocialRegister(admin.ModelAdmin):
    list_display = ('name', 'address', 'shop',)

class BuyProductRegister(admin.ModelAdmin):
    list_display = ('product',)
    search_fields = ('product', 'shop__username')

admin.site.register(Shop, ShopRegister)
admin.site.register(Category, CategoryRegister)
admin.site.register(Product, ProductRegister)
admin.site.register(Social, SocialRegister)
admin.site.register(BuyProduct, BuyProductRegister)