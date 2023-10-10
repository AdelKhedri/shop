from django.contrib import admin
from .models import Card, Cart, Transaction

# Register your models here.

class CardRegister(admin.ModelAdmin):
    list_display = ('user' ,'card_number',)
    search_fields = ("card_number", "shaba_number", "user")

class CartRegister(admin.ModelAdmin):
    list_display = ('customer', 'product', 'count',)
    search_fields = ("customer","product",)

class TransactionRegister(admin.ModelAdmin):
    list_display = ("transaction_type", "card", "amount", "teransaction_time", "is_payed",)
    list_filter= ("is_payed",)
    search_fields = ("ref_id",)

admin.site.register(Card, CardRegister)
admin.site.register(Cart, CartRegister)
admin.site.register(Transaction, TransactionRegister)