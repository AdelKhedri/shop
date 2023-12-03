import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
import time

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True, max_length=150, verbose_name="ایمیل")
    phone_number = models.BigIntegerField(unique=True, null=True, blank=True, verbose_name="شماره تلفن")
    is_active = models.BooleanField(default=False, verbose_name="اجازه ورود")
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'username', 'is_active']
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
    
    def __str__(self):
        return str(self.phone_number)

class Profile(models.Model):
    image = models.ImageField(upload_to="images/profiles/", default='images/profiles/default-image-profile.png', blank=True, null=True,verbose_name="عکس پروفایل")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coin = models.IntegerField(default=120000, verbose_name="موجودی(ریال)")
    invaited =  models.CharField(max_length=100, verbose_name="افراد دعوت شده", blank=True, null=True)
    nashnalcode = models.IntegerField(blank=True, null=True, verbose_name="کد ملی")

    def is_invaited(self):
        if self.invaited is not None:
            return True if len(self.invaited) > 1 else False
        else:
            return False

    def _str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['user', 'coin']
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل ها"
    

class OtpTypeChice(models.TextChoices):
    sinup = 'sinup', 'sinup'
    password = 'f_password', 'forget password'


class Otp(models.Model):
    number = models.BigIntegerField(verbose_name="شماره موبایل")
    code = models.IntegerField(verbose_name="کد تایید")
    expire_time = models.DateTimeField(verbose_name="زمان انقضا")
    otp_type = models.CharField(choices=OtpTypeChice.choices, max_length=10)
    
    class Meta:
        verbose_name = "کد تایید شماره"
        verbose_name_plural = "کد های تایید شماره"

    def __str__(self):
        return str(self.number)
    

class Notifacation(models.Model):
    reciver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="دریافت کننده")
    message = models.TextField(max_length=800, verbose_name="متن اعلان")
    color_list = (("bg-danger", "danger"),
                  ("bg-warning", "warning"),
                  ("bg-success", "success"),
                  ("bg-info", "info"),
                  ("bg-secondary", "seccondry"),
                  ("bg-primary", "primary")
                  )
    color = models.CharField(choices=color_list, default="info", max_length=12, verbose_name="رنگ" )

    class Meta:
        verbose_name = "نوتیفیکیشن"
        verbose_name_plural = "نوتیفیکیشن ها"
    
    def __str__(self):
        return str(self.reciver.phone_number)


class Support(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender",verbose_name="ارسال کننده")
    reciver = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="reciver", verbose_name="دریافت کننده")
    message = models.TextField(max_length=500, verbose_name="متن پیام")
    email = models.CharField(blank=True, null=True, max_length=150, verbose_name="ایمیل")
    send_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ارسال")

    class Meta:
        ordering = ['send_time']
        verbose_name = "کامند پشتیبانی"
        verbose_name_plural = "کامند های پشتیبانی"
    def __str__(self):
        return self.sender.username




# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="")
#     product = models.ForeignKey()