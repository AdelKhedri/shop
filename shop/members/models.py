from django.db import models
from django.contrib.auth.models import AbstractUser
import time

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True, max_length=150, verbose_name="ایمیل")
    phone_number = models.IntegerField(unique=True, null=True, blank=True, verbose_name="شماره تلفن")
    is_active = models.BooleanField(default=False, verbose_name="اجازه ورود")

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

class Profile(models.Model):
    image = models.ImageField(upload_to="images/profiles/", verbose_name="")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coin = models.IntegerField(default=0, verbose_name="")
    invaited =  models.CharField(max_length=100, verbose_name="", blank=True, null=True)
    nashnalcode = models.IntegerField(blank=True, null=True, verbose_name="")

    def is_invaited(self):
        return True if len(self.invaited) > 1 else False

    def _str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['user', 'coin']
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل ها"

class Otp(models.Model):
    number = models.IntegerField()
    code = models.IntegerField(verbose_name="")
    expire_time = models.DateTimeField(default=int(time.time())+300, verbose_name="")

    def __str__(self):
        return self.number
    
    class Meta:
        verbose_name = "کد تایید شماره"
        verbose_name_plural = "کد های تایید شماره"

class Notifacation(models.Model):
    reciver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="")
    message = models.TextField(max_length=800, verbose_name="")
    color_list = (("bg-danger", "danger"),
                  ("bg-warning", "warning"),
                  ("bg-success", "success"),
                  ("bg-info", "info"),
                  ("bg-secondary", "seccondry"),
                  ("bg-primary", "primary")
                  )
    color = models.CharField(choices=color_list, default="info", max_length=12, verbose_name="" )

    class Meta:
        verbose_name = "نوتیفیکیشن"
        verbose_name_plural = "نوتیفیکیشن ها"












# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="")
#     product = models.ForeignKey()