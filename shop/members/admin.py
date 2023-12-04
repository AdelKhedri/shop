from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from .models import User, Profile, Otp, Notifacation, Support, BlockIPAddress
from mylib.functions import get_ipaddress
from django.http import HttpResponseRedirect


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


class MyAdminSite(admin.AdminSite):
    def login(self, request, extra_context = None):
        ipaddress = get_ipaddress(request)
        if BlockIPAddress.objects.filter(ipaddress=ipaddress).exists():
            return HttpResponseRedirect('/404')
        return super().login(request, extra_context)


admin.site.register(User, UserRegister)
admin.site.register(Profile, ProfileRegister)
admin.site.register(Otp)
admin.site.register(Support)
admin.site.register(Notifacation, NotifacationRegister)
admin.site.register(BlockIPAddress)