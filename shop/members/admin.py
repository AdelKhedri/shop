from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Otp, Notifacation, Support

class UserRegister(admin.ModelAdmin):
    list_display = ('phone_number',)

class ProfileRegister(admin.ModelAdmin):
    list_display = ('user', 'coin', 'nashnalcode', 'is_invaited')
    # list_filter = ('is_invaited',)
    search_fields = ('user', 'nashnal', 'invaited')
    ordering = ['user']

class NotifacationRegister(admin.ModelAdmin):
    list_display = ('reciver', 'color',)
    list_filter = ('color',)
    search_fields = ('color',)
    ordering = ['reciver']
    
admin.site.register(User, UserRegister)
admin.site.register(Profile, ProfileRegister)
admin.site.register(Otp)
admin.site.register(Support)
admin.site.register(Notifacation, NotifacationRegister)

# Register your models here.
