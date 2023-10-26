from django.db import models
from members.models import User
from ShopApp.models import Product, Shop

# Create your models here.

class Card(models.Model):
    card_number = models.IntegerField(verbose_name="شماره کارت")
    shaba_number = models.CharField(max_length=24, verbose_name="شماره شبا")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="کاربر")

    class Meta:
        verbose_name = "کارت بانکی"
        verbose_name_plural = "کارت های بانکی"
    
    def __str__(self):
        return str(self.card_number)


class Transaction(models.Model):
    transaction_type_list = (('withdraw', 'برداشت'), ('deposit', 'پرداخت'))
    transaction_type = models.CharField(max_length=8, choices=transaction_type_list, verbose_name="نوع تراکنش")
    card = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name="کارت پرداخت کننده")
    amount = models.IntegerField(verbose_name="مقدار")
    transaction_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان تراکنش")
    is_payed = models.BooleanField(default=False, verbose_name="پرداخت شده")
    ref_id = models.IntegerField(null=True, blank=True ,verbose_name="ای دی رف")
    description = models.CharField(null=True, blank=True ,max_length=300, verbose_name="جزییات")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="فروشگاه")

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش ها"
        ordering = ['transaction_time']
    
    def __str__(self):
        return self.card.user.username


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="خریدار")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    count = models.IntegerField(default=1, verbose_name="تعداد")

    class Meta:
        verbose_name = "سبدخرید"
        verbose_name_plural = "سبد های خرید"
    
    def __str__(self):
        return self.customer.username



class Likes(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    
    class Meta:
        verbose_name = 'پسندیده'
        verbose_name_plural = 'پسندیده ها'
        ordering = ['product__name']

    def __str__(self):
        return self.product.name