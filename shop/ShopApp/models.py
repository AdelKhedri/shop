from django.db import models
from members.models import User
# Create your models here.

class Shop(models.Model):
    name = models.CharField(max_length=150, verbose_name="نام ")
    username = models.CharField(max_length=150, unique=True, verbose_name="ایدی")
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name="درباره")
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="مدیر")
    small_image = models.ImageField(upload_to='images/shops/',null=True, blank=True, verbose_name="عکس")
    banner_image = models.ImageField(upload_to='images/shops/',null=True, blank=True, verbose_name="بنر")
    is_active = models.BooleanField(default=False, verbose_name="فعال")
    phone_number = models.IntegerField(null=True, blank=True, verbose_name="شماره تلفن")
    social_address_count = models.IntegerField(default=0, verbose_name="تعداد ادرس شبکه های اجتماعی")
    
    class Meta:
        verbose_name = "فروشگاه"
        verbose_name_plural = "فروشگاها"
    
    def __str__(self):
        return self.name


class Social(models.Model):
    social_list = (('instagram.com/', 'اینستاگرام'),
                   ('t.me/', 'تلگرام'),
                   ('snapchat.com/add/', 'اسنپ چت'),
                   ('wa.me/', 'واتساپ'),
                   ('Facebook.com/', 'فیسبوک'),
                #    ('instagram.com/', 'اینستاگرام'),
                #    ('instagram.com/', 'اینستاگرام'),
                #    ('instagram.com/', 'اینستاگرام'),
                #    ('instagram.com/', 'اینستاگرام'),
                #    ('instagram.com/', 'اینستاگرام'),
                #    ('instagram.com/', 'اینستاگرام'),
                #    ('instagram.com/', 'اینستاگرام'),
                #    ('instagram.com/', 'اینستاگرام'),
                #    ('instagram.com/', 'اینستاگرام'),
                #    ('instagram.com/', 'اینستاگرام'),
                #    ('instagram.com/', 'اینستاگرام'),
                #    ('instagram.com/', 'اینستاگرام'),
                #    ('instagram.com/', 'اینستاگرام'),
                #    ('instagram.com/', 'اینستاگرام'),
                #    ('instagram.com/', 'اینستاگرام'),
                  )
    name = models.CharField(max_length=100, choices=social_list, verbose_name="نام")
    address = models.CharField(max_length=100, verbose_name="نام کاربری")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="فروشگاه")

    class Meta:
        verbose_name = "آدرس شبکه اجتماعی"
        verbose_name_plural = "آدرس شبکه های اجتماعی"
    
    def __str__(self):
        return f"{self.name} of {self.shop}"

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="نام")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="فروشگاه")
    for_sell = models.BooleanField(default=False, verbose_name="برای نمایش در صفحه اول فروشگاه")
    number_ordering = models.IntegerField(verbose_name="شماره ردیف",null=True, blank=True)
    
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="نام")
    max_sel = models.IntegerField(null=True, blank=True, verbose_name="حداکثر فروش(تعداد فروش)")
    price = models.IntegerField(default=0, verbose_name="قیمت")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="فروشگاه")
    category = models.ForeignKey(Category,null=True, blank=True, on_delete=models.CASCADE, verbose_name="دسته بندی")
    description = models.CharField(max_length=400,null=True, blank=True, verbose_name="درباره")
    class Meta:
        verbose_name = "محضول"
        verbose_name_plural = "محصولات"
        ordering = ['name']
    
    def __str__(self):
        return self.name